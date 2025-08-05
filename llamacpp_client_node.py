import json
import requests
import base64
from typing import Dict, Any, List, Optional, Union
import io
from PIL import Image


class LlamaCppClientNode:
    """
    ComfyUI custom node that acts as a client for llama-server from llama.cpp.
    Supports ALL possible parameters that llama-server accepts through its various endpoints.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "server_url": ("STRING", {
                    "default": "http://127.0.0.1:8080",
                    "multiline": False,
                    "tooltip": "Base URL of the llama-server instance"
                }),
                "endpoint": (["completion", "chat_completions", "embeddings", "tokenize", "detokenize", "apply_template", "infill", "reranking"], {
                    "default": "completion",
                    "tooltip": "API endpoint to use"
                }),
                "prompt": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "The prompt text for completion/chat"
                }),
            },
            "optional": {
                # Connection & Auth
                "api_key": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "API key for authentication (if required)"
                }),
                "timeout": ("INT", {
                    "default": 600,
                    "min": 1,
                    "max": 3600,
                    "tooltip": "Request timeout in seconds"
                }),
                
                # Core Generation Parameters
                "n_predict": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 100000,
                    "tooltip": "Number of tokens to predict (-1 = infinity)"
                }),
                "temperature": ("FLOAT", {
                    "default": 0.8,
                    "min": 0.0,
                    "max": 10.0,
                    "step": 0.01,
                    "tooltip": "Sampling temperature"
                }),
                "top_k": ("INT", {
                    "default": 40,
                    "min": 0,
                    "max": 1000,
                    "tooltip": "Top-k sampling"
                }),
                "top_p": ("FLOAT", {
                    "default": 0.95,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Top-p (nucleus) sampling"
                }),
                "min_p": ("FLOAT", {
                    "default": 0.05,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Min-p sampling"
                }),
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2**31-1,
                    "tooltip": "Random seed (-1 for random)"
                }),
                
                # Dynamic Temperature
                "dynatemp_range": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.01,
                    "tooltip": "Dynamic temperature range"
                }),
                "dynatemp_exponent": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.1,
                    "max": 10.0,
                    "step": 0.01,
                    "tooltip": "Dynamic temperature exponent"
                }),
                
                # XTC Sampling
                "xtc_probability": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "XTC probability"
                }),
                "xtc_threshold": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "XTC threshold"
                }),
                
                # Repetition Control
                "repeat_penalty": ("FLOAT", {
                    "default": 1.1,
                    "min": 0.1,
                    "max": 5.0,
                    "step": 0.01,
                    "tooltip": "Repetition penalty"
                }),
                "repeat_last_n": ("INT", {
                    "default": 64,
                    "min": -1,
                    "max": 2048,
                    "tooltip": "Last n tokens for repetition penalty"
                }),
                "presence_penalty": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Presence penalty"
                }),
                "frequency_penalty": ("FLOAT", {
                    "default": 0.0,
                    "min": -2.0,
                    "max": 2.0,
                    "step": 0.01,
                    "tooltip": "Frequency penalty"
                }),
                
                # DRY Sampling
                "dry_multiplier": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 5.0,
                    "step": 0.01,
                    "tooltip": "DRY sampling multiplier"
                }),
                "dry_base": ("FLOAT", {
                    "default": 1.75,
                    "min": 1.0,
                    "max": 5.0,
                    "step": 0.01,
                    "tooltip": "DRY sampling base value"
                }),
                "dry_allowed_length": ("INT", {
                    "default": 2,
                    "min": 1,
                    "max": 100,
                    "tooltip": "DRY allowed length"
                }),
                "dry_penalty_last_n": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2048,
                    "tooltip": "DRY penalty last n tokens"
                }),
                "dry_sequence_breakers": ("STRING", {
                    "default": '["\\n", ":", "\\"", "*"]',
                    "multiline": False,
                    "tooltip": "JSON array of DRY sequence breakers"
                }),
                
                # Mirostat
                "mirostat": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 2,
                    "tooltip": "Mirostat sampling (0=disabled, 1=v1, 2=v2)"
                }),
                "mirostat_tau": ("FLOAT", {
                    "default": 5.0,
                    "min": 0.1,
                    "max": 20.0,
                    "step": 0.1,
                    "tooltip": "Mirostat target entropy"
                }),
                "mirostat_eta": ("FLOAT", {
                    "default": 0.1,
                    "min": 0.001,
                    "max": 1.0,
                    "step": 0.001,
                    "tooltip": "Mirostat learning rate"
                }),
                
                # Other Sampling
                "typical_p": ("FLOAT", {
                    "default": 1.0,
                    "min": 0.0,
                    "max": 1.0,
                    "step": 0.01,
                    "tooltip": "Locally typical sampling"
                }),
                
                # Control Parameters
                "n_keep": ("INT", {
                    "default": 0,
                    "min": -1,
                    "max": 2048,
                    "tooltip": "Number of tokens to keep from prompt"
                }),
                "stop_sequences": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                    "tooltip": "JSON array of stop sequences"
                }),
                "ignore_eos": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Ignore end-of-stream token"
                }),
                
                # Streaming and Output
                "stream": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Enable streaming mode"
                }),
                "n_probs": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 100,
                    "tooltip": "Return top N token probabilities"
                }),
                "min_keep": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 100,
                    "tooltip": "Minimum tokens to keep in sampler"
                }),
                "post_sampling_probs": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Return post-sampling probabilities"
                }),
                "return_tokens": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Return raw token IDs"
                }),
                "timings_per_token": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Include timing information"
                }),
                
                # Grammar and JSON
                "grammar": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "BNF grammar for constrained generation"
                }),
                "json_schema": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "JSON schema for constrained generation"
                }),
                
                # Logit Bias
                "logit_bias": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                    "tooltip": "JSON array of logit bias modifications"
                }),
                
                # Cache and Slot Management
                "cache_prompt": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Re-use KV cache from previous requests"
                }),
                "id_slot": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 100,
                    "tooltip": "Assign to specific slot (-1 = auto)"
                }),
                
                # Sampler Order
                "samplers": ("STRING", {
                    "default": '["dry", "top_k", "typ_p", "top_p", "min_p", "xtc", "temperature"]',
                    "multiline": False,
                    "tooltip": "JSON array defining sampler order"
                }),
                
                # Timing Constraints
                "t_max_predict_ms": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 60000,
                    "tooltip": "Maximum prediction time in milliseconds"
                }),
                
                # Chat-specific parameters
                "messages": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                    "tooltip": "JSON array of chat messages (for chat_completions endpoint)"
                }),
                "system_message": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "System message for chat"
                }),
                "user_message": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "User message for chat"
                }),
                "assistant_message": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Assistant message for chat (for prefilling)"
                }),
                "max_tokens": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 100000,
                    "tooltip": "Maximum tokens in response (OpenAI style)"
                }),
                "model": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "tooltip": "Model name/alias"
                }),
                
                # Function calling
                "tools": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                    "tooltip": "JSON array of available tools/functions"
                }),
                "tool_choice": ("STRING", {
                    "default": "auto",
                    "multiline": False,
                    "tooltip": "Tool choice strategy"
                }),
                
                # Response format
                "response_format": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "JSON object defining response format"
                }),
                
                # Embeddings-specific
                "input_text": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Input text for embeddings"
                }),
                "encoding_format": (["float", "base64"], {
                    "default": "float",
                    "tooltip": "Encoding format for embeddings"
                }),
                "embd_normalize": ("INT", {
                    "default": 2,
                    "min": -1,
                    "max": 10,
                    "tooltip": "Embedding normalization type"
                }),
                
                # Tokenization
                "content": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Content to tokenize/detokenize"
                }),
                "tokens": ("STRING", {
                    "default": "[]",
                    "multiline": False,
                    "tooltip": "JSON array of token IDs"
                }),
                "add_special": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Add special tokens during tokenization"
                }),
                "parse_special": ("BOOLEAN", {
                    "default": True,
                    "tooltip": "Parse special tokens during tokenization"
                }),
                "with_pieces": ("BOOLEAN", {
                    "default": False,
                    "tooltip": "Return token pieces with IDs"
                }),
                
                # Infill-specific
                "input_prefix": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Code prefix for infill"
                }),
                "input_suffix": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Code suffix for infill"
                }),
                "input_extra": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                    "tooltip": "JSON array of additional context files"
                }),
                
                # Reranking-specific
                "query": ("STRING", {
                    "default": "",
                    "multiline": True,
                    "tooltip": "Query for reranking"
                }),
                "documents": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                    "tooltip": "JSON array of documents to rank"
                }),
                "top_n": ("INT", {
                    "default": 10,
                    "min": 1,
                    "max": 1000,
                    "tooltip": "Number of top results to return"
                }),
                
                # LoRA adapters
                "lora": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                    "tooltip": "JSON array of LoRA adapter configurations"
                }),
                
                # Response fields selection
                "response_fields": ("STRING", {
                    "default": "[]",
                    "multiline": False,
                    "tooltip": "JSON array of specific response fields to return"
                }),
                
                # Multimodal support
                "image_data": ("STRING", {
                    "default": "[]",
                    "multiline": True,
                    "tooltip": "JSON array of image data objects"
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("response", "raw_response", "error", "status_code")
    FUNCTION = "process_request"
    CATEGORY = "AI/LlamaCpp"
    
    def process_request(self, server_url: str, endpoint: str, prompt: str, **kwargs):
        """Process the request to llama-server with all provided parameters."""
        
        try:
            # Clean up server URL
            server_url = server_url.rstrip('/')
            
            # Build the request based on endpoint
            if endpoint == "completion":
                response, raw_response, error, status_code = self._handle_completion(server_url, prompt, **kwargs)
            elif endpoint == "chat_completions":
                response, raw_response, error, status_code = self._handle_chat_completions(server_url, **kwargs)
            elif endpoint == "embeddings":
                response, raw_response, error, status_code = self._handle_embeddings(server_url, **kwargs)
            elif endpoint == "tokenize":
                response, raw_response, error, status_code = self._handle_tokenize(server_url, **kwargs)
            elif endpoint == "detokenize":
                response, raw_response, error, status_code = self._handle_detokenize(server_url, **kwargs)
            elif endpoint == "apply_template":
                response, raw_response, error, status_code = self._handle_apply_template(server_url, **kwargs)
            elif endpoint == "infill":
                response, raw_response, error, status_code = self._handle_infill(server_url, **kwargs)
            elif endpoint == "reranking":
                response, raw_response, error, status_code = self._handle_reranking(server_url, **kwargs)
            else:
                return "", "", f"Unsupported endpoint: {endpoint}", 400
                
            return response, raw_response, error, status_code
            
        except Exception as e:
            return "", "", f"Error processing request: {str(e)}", 500
    
    def _make_request(self, url: str, data: Dict[str, Any], api_key: str = "", timeout: int = 600):
        """Make HTTP request to llama-server."""
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=timeout)
            return response.json(), json.dumps(response.json(), indent=2), "", response.status_code
        except requests.exceptions.Timeout:
            return "", "", "Request timeout", 408
        except requests.exceptions.ConnectionError:
            return "", "", "Connection error", 503
        except requests.exceptions.RequestException as e:
            return "", "", f"Request error: {str(e)}", 500
        except json.JSONDecodeError:
            return "", response.text if 'response' in locals() else "", "Invalid JSON response", 502
    
    def _clean_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Remove None values and convert string parameters to appropriate types."""
        cleaned = {}
        
        for key, value in params.items():
            if value is None:
                continue
                
            # Handle string parameters that should be parsed as JSON
            if key in ['stop_sequences', 'logit_bias', 'samplers', 'messages', 'tools', 
                      'response_format', 'input_extra', 'documents', 'lora', 'response_fields',
                      'image_data', 'dry_sequence_breakers', 'tokens']:
                if isinstance(value, str) and value.strip():
                    try:
                        cleaned[key] = json.loads(value)
                    except json.JSONDecodeError:
                        continue
            else:
                cleaned[key] = value
        
        return cleaned
    
    def _handle_completion(self, server_url: str, prompt: str, **kwargs):
        """Handle /completion endpoint."""
        url = f"{server_url}/completion"
        
        # Build parameters
        params = {
            "prompt": prompt,
        }
        
        # Add all relevant parameters
        param_mapping = {
            "n_predict": "n_predict",
            "temperature": "temperature", 
            "top_k": "top_k",
            "top_p": "top_p",
            "min_p": "min_p",
            "seed": "seed",
            "dynatemp_range": "dynatemp_range",
            "dynatemp_exponent": "dynatemp_exponent",
            "xtc_probability": "xtc_probability",
            "xtc_threshold": "xtc_threshold",
            "repeat_penalty": "repeat_penalty",
            "repeat_last_n": "repeat_last_n",
            "presence_penalty": "presence_penalty",
            "frequency_penalty": "frequency_penalty",
            "dry_multiplier": "dry_multiplier",
            "dry_base": "dry_base",
            "dry_allowed_length": "dry_allowed_length",
            "dry_penalty_last_n": "dry_penalty_last_n",
            "dry_sequence_breakers": "dry_sequence_breakers",
            "mirostat": "mirostat",
            "mirostat_tau": "mirostat_tau",
            "mirostat_eta": "mirostat_eta",
            "typical_p": "typical_p",
            "n_keep": "n_keep",
            "stop_sequences": "stop",
            "ignore_eos": "ignore_eos",
            "stream": "stream",
            "n_probs": "n_probs",
            "min_keep": "min_keep",
            "post_sampling_probs": "post_sampling_probs",
            "return_tokens": "return_tokens",
            "timings_per_token": "timings_per_token",
            "grammar": "grammar",
            "json_schema": "json_schema",
            "logit_bias": "logit_bias",
            "cache_prompt": "cache_prompt",
            "id_slot": "id_slot",
            "samplers": "samplers",
            "t_max_predict_ms": "t_max_predict_ms",
            "lora": "lora",
            "response_fields": "response_fields",
            "image_data": "image_data",
        }
        
        for param_key, api_key in param_mapping.items():
            if param_key in kwargs and kwargs[param_key] is not None:
                if param_key == "stop_sequences":
                    params[api_key] = kwargs[param_key]
                else:
                    params[api_key] = kwargs[param_key]
        
        # Clean parameters
        params = self._clean_params(params)
        
        return self._make_request(url, params, kwargs.get("api_key", ""), kwargs.get("timeout", 600))
    
    def _handle_chat_completions(self, server_url: str, **kwargs):
        """Handle /v1/chat/completions endpoint."""
        url = f"{server_url}/v1/chat/completions"
        
        # Build messages array
        messages = []
        
        # Parse existing messages if provided
        if kwargs.get("messages") and kwargs["messages"].strip():
            try:
                messages = json.loads(kwargs["messages"])
            except json.JSONDecodeError:
                pass
        
        # Add individual messages if provided
        if kwargs.get("system_message") and kwargs["system_message"].strip():
            messages.append({"role": "system", "content": kwargs["system_message"]})
        
        if kwargs.get("user_message") and kwargs["user_message"].strip():
            messages.append({"role": "user", "content": kwargs["user_message"]})
        
        if kwargs.get("assistant_message") and kwargs["assistant_message"].strip():
            messages.append({"role": "assistant", "content": kwargs["assistant_message"]})
        
        # If no messages, use prompt as user message
        if not messages and kwargs.get("prompt"):
            messages.append({"role": "user", "content": kwargs["prompt"]})
        
        params = {
            "messages": messages,
            "model": kwargs.get("model", "default"),
        }
        
        # Add chat-specific parameters
        param_mapping = {
            "max_tokens": "max_tokens",
            "temperature": "temperature",
            "top_p": "top_p",
            "top_k": "top_k",
            "min_p": "min_p",
            "seed": "seed",
            "stream": "stream",
            "stop_sequences": "stop",
            "presence_penalty": "presence_penalty",
            "frequency_penalty": "frequency_penalty",
            "tools": "tools",
            "tool_choice": "tool_choice",
            "response_format": "response_format",
            "n_probs": "logprobs",
        }
        
        for param_key, api_key in param_mapping.items():
            if param_key in kwargs and kwargs[param_key] is not None:
                params[api_key] = kwargs[param_key]
        
        # Clean parameters
        params = self._clean_params(params)
        
        return self._make_request(url, params, kwargs.get("api_key", ""), kwargs.get("timeout", 600))
    
    def _handle_embeddings(self, server_url: str, **kwargs):
        """Handle /v1/embeddings endpoint."""
        url = f"{server_url}/v1/embeddings"
        
        # Use input_text or content or prompt
        input_text = kwargs.get("input_text") or kwargs.get("content") or kwargs.get("prompt", "")
        
        params = {
            "input": input_text,
            "model": kwargs.get("model", "default"),
            "encoding_format": kwargs.get("encoding_format", "float"),
        }
        
        # Clean parameters
        params = self._clean_params(params)
        
        return self._make_request(url, params, kwargs.get("api_key", ""), kwargs.get("timeout", 600))
    
    def _handle_tokenize(self, server_url: str, **kwargs):
        """Handle /tokenize endpoint."""
        url = f"{server_url}/tokenize"
        
        content = kwargs.get("content") or kwargs.get("prompt", "")
        
        params = {
            "content": content,
            "add_special": kwargs.get("add_special", False),
            "parse_special": kwargs.get("parse_special", True),
            "with_pieces": kwargs.get("with_pieces", False),
        }
        
        return self._make_request(url, params, kwargs.get("api_key", ""), kwargs.get("timeout", 600))
    
    def _handle_detokenize(self, server_url: str, **kwargs):
        """Handle /detokenize endpoint."""
        url = f"{server_url}/detokenize"
        
        tokens = kwargs.get("tokens", "[]")
        if isinstance(tokens, str):
            try:
                tokens = json.loads(tokens)
            except json.JSONDecodeError:
                tokens = []
        
        params = {
            "tokens": tokens,
        }
        
        return self._make_request(url, params, kwargs.get("api_key", ""), kwargs.get("timeout", 600))
    
    def _handle_apply_template(self, server_url: str, **kwargs):
        """Handle /apply-template endpoint."""
        url = f"{server_url}/apply-template"
        
        messages = kwargs.get("messages", "[]")
        if isinstance(messages, str):
            try:
                messages = json.loads(messages)
            except json.JSONDecodeError:
                messages = []
        
        params = {
            "messages": messages,
        }
        
        return self._make_request(url, params, kwargs.get("api_key", ""), kwargs.get("timeout", 600))
    
    def _handle_infill(self, server_url: str, **kwargs):
        """Handle /infill endpoint."""
        url = f"{server_url}/infill"
        
        params = {
            "input_prefix": kwargs.get("input_prefix", ""),
            "input_suffix": kwargs.get("input_suffix", ""),
        }
        
        if kwargs.get("input_extra"):
            try:
                params["input_extra"] = json.loads(kwargs["input_extra"])
            except json.JSONDecodeError:
                pass
        
        if kwargs.get("prompt"):
            params["prompt"] = kwargs["prompt"]
        
        # Add completion parameters
        completion_params = [
            "temperature", "top_k", "top_p", "min_p", "seed", "stream",
            "n_predict", "stop_sequences", "repeat_penalty", "repeat_last_n"
        ]
        
        for param in completion_params:
            if param in kwargs and kwargs[param] is not None:
                if param == "stop_sequences":
                    params["stop"] = kwargs[param]
                else:
                    params[param] = kwargs[param]
        
        # Clean parameters
        params = self._clean_params(params)
        
        return self._make_request(url, params, kwargs.get("api_key", ""), kwargs.get("timeout", 600))
    
    def _handle_reranking(self, server_url: str, **kwargs):
        """Handle /v1/rerank endpoint."""
        url = f"{server_url}/v1/rerank"
        
        query = kwargs.get("query", "")
        documents = kwargs.get("documents", "[]")
        
        if isinstance(documents, str):
            try:
                documents = json.loads(documents)
            except json.JSONDecodeError:
                documents = []
        
        params = {
            "model": kwargs.get("model", "default"),
            "query": query,
            "documents": documents,
            "top_n": kwargs.get("top_n", 10),
        }
        
        return self._make_request(url, params, kwargs.get("api_key", ""), kwargs.get("timeout", 600))


# Node mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "LlamaCppClient": LlamaCppClientNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LlamaCppClient": "Llama.cpp Server Client"
}
