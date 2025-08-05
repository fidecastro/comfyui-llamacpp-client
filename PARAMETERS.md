# Complete Parameter Reference

This document provides a comprehensive reference for all parameters supported by the LlamaCpp Client Node.

## Connection Parameters

### server_url (STRING, required)
- **Default**: `"http://127.0.0.1:8080"`
- **Description**: Base URL of the llama-server instance
- **Example**: `"http://localhost:8080"`, `"https://my-server.com:8080"`

### api_key (STRING, optional)
- **Default**: `""`
- **Description**: API key for authentication if required by server
- **Example**: `"sk-your-api-key-here"`

### timeout (INT, optional)
- **Default**: `600`
- **Range**: 1-3600
- **Description**: Request timeout in seconds
- **Usage**: Increase for long generations

## Core Generation Parameters

### prompt (STRING, required)
- **Default**: `""`
- **Description**: The main input text for generation
- **Multiline**: Yes
- **Usage**: Primary input for completion and infill endpoints

### n_predict (INT, optional)
- **Default**: `-1`
- **Range**: -1 to 100000
- **Description**: Maximum number of tokens to generate
- **Special**: -1 = unlimited generation

### temperature (FLOAT, optional)
- **Default**: `0.8`
- **Range**: 0.0-10.0
- **Step**: 0.01
- **Description**: Controls randomness in generation
- **Usage**: Lower = more deterministic, Higher = more creative

### seed (INT, optional)
- **Default**: `-1`
- **Range**: -1 to 2^31-1
- **Description**: Random seed for reproducible generation
- **Special**: -1 = random seed

## Sampling Parameters

### top_k (INT, optional)
- **Default**: `40`
- **Range**: 0-1000
- **Description**: Limit selection to top K most probable tokens
- **Special**: 0 = disabled

### top_p (FLOAT, optional)
- **Default**: `0.95`
- **Range**: 0.0-1.0
- **Step**: 0.01
- **Description**: Nucleus sampling - cumulative probability threshold
- **Usage**: 1.0 = disabled

### min_p (FLOAT, optional)
- **Default**: `0.05`
- **Range**: 0.0-1.0
- **Step**: 0.01
- **Description**: Minimum probability relative to most likely token
- **Usage**: 0.0 = disabled

### typical_p (FLOAT, optional)
- **Default**: `1.0`
- **Range**: 0.0-1.0
- **Step**: 0.01
- **Description**: Locally typical sampling parameter
- **Usage**: 1.0 = disabled

## Dynamic Temperature

### dynatemp_range (FLOAT, optional)
- **Default**: `0.0`
- **Range**: 0.0-5.0
- **Step**: 0.01
- **Description**: Dynamic temperature variation range
- **Usage**: Final temp = temperature ± dynatemp_range

### dynatemp_exponent (FLOAT, optional)
- **Default**: `1.0`
- **Range**: 0.1-10.0
- **Step**: 0.01
- **Description**: Controls dynamic temperature curve shape

## XTC (Cross-Token Coherence) Sampling

### xtc_probability (FLOAT, optional)
- **Default**: `0.0`
- **Range**: 0.0-1.0
- **Step**: 0.01
- **Description**: Probability of token removal via XTC
- **Usage**: 0.0 = disabled

### xtc_threshold (FLOAT, optional)
- **Default**: `0.1`
- **Range**: 0.0-1.0
- **Step**: 0.01
- **Description**: Minimum probability threshold for XTC
- **Usage**: >0.5 effectively disables XTC

## Repetition Control

### repeat_penalty (FLOAT, optional)
- **Default**: `1.1`
- **Range**: 0.1-5.0
- **Step**: 0.01
- **Description**: Penalty for repeating token sequences
- **Usage**: >1.0 = discourage repetition, <1.0 = encourage

### repeat_last_n (INT, optional)
- **Default**: `64`
- **Range**: -1 to 2048
- **Description**: Number of recent tokens to consider for repetition
- **Special**: 0 = disabled, -1 = context size

### presence_penalty (FLOAT, optional)
- **Default**: `0.0`
- **Range**: -2.0 to 2.0
- **Step**: 0.01
- **Description**: OpenAI-style presence penalty
- **Usage**: Positive = discourage token presence

### frequency_penalty (FLOAT, optional)
- **Default**: `0.0`
- **Range**: -2.0 to 2.0
- **Step**: 0.01
- **Description**: OpenAI-style frequency penalty
- **Usage**: Positive = discourage frequent tokens

## DRY (Don't Repeat Yourself) Sampling

### dry_multiplier (FLOAT, optional)
- **Default**: `0.0`
- **Range**: 0.0-5.0
- **Step**: 0.01
- **Description**: DRY repetition penalty strength
- **Usage**: 0.0 = disabled

### dry_base (FLOAT, optional)
- **Default**: `1.75`
- **Range**: 1.0-5.0
- **Step**: 0.01
- **Description**: Base value for DRY penalty calculation

### dry_allowed_length (INT, optional)
- **Default**: `2`
- **Range**: 1-100
- **Description**: Minimum repetition length before penalty applies

### dry_penalty_last_n (INT, optional)
- **Default**: `-1`
- **Range**: -1 to 2048
- **Description**: Context window for DRY penalty
- **Special**: 0 = disabled, -1 = context size

### dry_sequence_breakers (STRING, optional)
- **Default**: `'["\\n", ":", "\\"", "*"]'`
- **Format**: JSON array of strings
- **Description**: Sequences that break repetition detection
- **Example**: `'["\\n", ".", "!", "?"]'`

## Mirostat Sampling

### mirostat (INT, optional)
- **Default**: `0`
- **Range**: 0-2
- **Description**: Mirostat sampling mode
- **Values**: 0 = disabled, 1 = Mirostat v1, 2 = Mirostat v2

### mirostat_tau (FLOAT, optional)
- **Default**: `5.0`
- **Range**: 0.1-20.0
- **Step**: 0.1
- **Description**: Mirostat target entropy (tau parameter)

### mirostat_eta (FLOAT, optional)
- **Default**: `0.1`
- **Range**: 0.001-1.0
- **Step**: 0.001
- **Description**: Mirostat learning rate (eta parameter)

## Control Parameters

### n_keep (INT, optional)
- **Default**: `0`
- **Range**: -1 to 2048
- **Description**: Tokens to keep when context is exceeded
- **Special**: -1 = keep all, 0 = keep none

### stop_sequences (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of strings
- **Description**: Stop generation when these sequences are encountered
- **Example**: `'["\\n", "END", "STOP"]'`

### ignore_eos (BOOLEAN, optional)
- **Default**: `false`
- **Description**: Continue generation after end-of-stream token

## Streaming and Output

### stream (BOOLEAN, optional)
- **Default**: `false`
- **Description**: Enable real-time token streaming

### n_probs (INT, optional)
- **Default**: `0`
- **Range**: 0-100
- **Description**: Return top N token probabilities

### min_keep (INT, optional)
- **Default**: `0`
- **Range**: 0-100
- **Description**: Minimum tokens samplers must keep

### post_sampling_probs (BOOLEAN, optional)
- **Default**: `false`
- **Description**: Return probabilities after sampling chain

### return_tokens (BOOLEAN, optional)
- **Default**: `false`
- **Description**: Include raw token IDs in response

### timings_per_token (BOOLEAN, optional)
- **Default**: `false`
- **Description**: Include detailed timing information

## Grammar and Constraints

### grammar (STRING, optional)
- **Default**: `""`
- **Format**: BNF grammar rules
- **Description**: Constrain generation using formal grammar
- **Multiline**: Yes

### json_schema (STRING, optional)
- **Default**: `""`
- **Format**: JSON Schema
- **Description**: Constrain generation to valid JSON
- **Multiline**: Yes
- **Example**: `'{"type": "object", "properties": {"name": {"type": "string"}}}'`

## Logit Bias

### logit_bias (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array
- **Description**: Modify token probabilities
- **Example**: `'[[15043, 1.0], ["Hello", -0.5]]'`
- **Usage**: Positive = increase probability, Negative = decrease

## Cache and Performance

### cache_prompt (BOOLEAN, optional)
- **Default**: `true`
- **Description**: Reuse KV cache from previous requests

### id_slot (INT, optional)
- **Default**: `-1`
- **Range**: -1 to 100
- **Description**: Assign to specific processing slot
- **Special**: -1 = automatic assignment

### t_max_predict_ms (INT, optional)
- **Default**: `0`
- **Range**: 0-60000
- **Description**: Maximum generation time in milliseconds
- **Special**: 0 = unlimited

## Sampler Configuration

### samplers (STRING, optional)
- **Default**: `'["dry", "top_k", "typ_p", "top_p", "min_p", "xtc", "temperature"]'`
- **Format**: JSON array of strings
- **Description**: Order of sampler application
- **Available**: dry, top_k, typ_p, top_p, min_p, xtc, temperature

## Chat-Specific Parameters

### messages (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of message objects
- **Description**: Full chat conversation history
- **Example**: `'[{"role": "user", "content": "Hello"}]'`

### system_message (STRING, optional)
- **Default**: `""`
- **Description**: System prompt for chat
- **Multiline**: Yes

### user_message (STRING, optional)
- **Default**: `""`
- **Description**: User input for chat
- **Multiline**: Yes

### assistant_message (STRING, optional)
- **Default**: `""`
- **Description**: Assistant response for prefilling
- **Multiline**: Yes

### max_tokens (INT, optional)
- **Default**: `-1`
- **Range**: -1 to 100000
- **Description**: OpenAI-style maximum token limit

### model (STRING, optional)
- **Default**: `""`
- **Description**: Model name or alias

## Function Calling

### tools (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of tool definitions
- **Description**: Available functions for the model to call
- **Multiline**: Yes

### tool_choice (STRING, optional)
- **Default**: `"auto"`
- **Description**: Tool selection strategy
- **Values**: "auto", "none", or specific tool name

### response_format (STRING, optional)
- **Default**: `""`
- **Format**: JSON object
- **Description**: Specify response format constraints
- **Multiline**: Yes

## Embeddings Parameters

### input_text (STRING, optional)
- **Default**: `""`
- **Description**: Text to generate embeddings for
- **Multiline**: Yes

### encoding_format (STRING, optional)
- **Default**: `"float"`
- **Values**: "float", "base64"
- **Description**: Format for embedding output

### embd_normalize (INT, optional)
- **Default**: `2`
- **Range**: -1 to 10
- **Description**: Embedding normalization method
- **Values**: -1=none, 0=max_abs, 1=taxicab, 2=euclidean, >2=p-norm

## Tokenization Parameters

### content (STRING, optional)
- **Default**: `""`
- **Description**: Content to tokenize or detokenize
- **Multiline**: Yes

### tokens (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of integers
- **Description**: Token IDs for detokenization

### add_special (BOOLEAN, optional)
- **Default**: `false`
- **Description**: Include special tokens (BOS, EOS) in tokenization

### parse_special (BOOLEAN, optional)
- **Default**: `true`
- **Description**: Parse special tokens during tokenization

### with_pieces (BOOLEAN, optional)
- **Default**: `false`
- **Description**: Return token text pieces with IDs

## Infill Parameters

### input_prefix (STRING, optional)
- **Default**: `""`
- **Description**: Code or text before the insertion point
- **Multiline**: Yes

### input_suffix (STRING, optional)
- **Default**: `""`
- **Description**: Code or text after the insertion point
- **Multiline**: Yes

### input_extra (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of file objects
- **Description**: Additional context files
- **Example**: `'[{"filename": "utils.py", "text": "def helper(): pass"}]'`

## Reranking Parameters

### query (STRING, optional)
- **Default**: `""`
- **Description**: Search query for document ranking
- **Multiline**: Yes

### documents (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of strings
- **Description**: Documents to rank by relevance
- **Multiline**: Yes

### top_n (INT, optional)
- **Default**: `10`
- **Range**: 1-1000
- **Description**: Number of top results to return

## LoRA Adapters

### lora (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of adapter objects
- **Description**: LoRA adapter configurations
- **Example**: `'[{"id": 0, "scale": 0.8}, {"id": 1, "scale": 0.5}]'`
- **Multiline**: Yes

## Advanced Options

### response_fields (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of strings
- **Description**: Specific response fields to return
- **Example**: `'["content", "generation_settings/n_predict"]'`

### image_data (STRING, optional)
- **Default**: `"[]"`
- **Format**: JSON array of image objects
- **Description**: Base64-encoded images for multimodal models
- **Example**: `'[{"data": "base64string", "id": 1}]'`
- **Multiline**: Yes

## Parameter Usage Tips

1. **Start Simple**: Begin with basic parameters (prompt, temperature, n_predict)
2. **Gradual Complexity**: Add advanced sampling parameters incrementally
3. **Model-Specific**: Some parameters may not work with all models
4. **Performance**: Complex sampling configurations may slow generation
5. **Validation**: Use test_node.py to verify parameter combinations
6. **Documentation**: Refer to llama-server documentation for latest features

## Common Parameter Combinations

### Creative Writing
```
temperature: 0.9
top_p: 0.95
dynatemp_range: 0.3
dry_multiplier: 0.8
repeat_penalty: 1.05
```

### Code Generation
```
temperature: 0.2
top_p: 0.8
top_k: 20
repeat_penalty: 1.1
```

### Factual Q&A
```
temperature: 0.1
top_p: 0.9
mirostat: 2
mirostat_tau: 3.0
```

### Structured Output
```
temperature: 0.7
json_schema: {schema_here}
n_predict: 200
```
