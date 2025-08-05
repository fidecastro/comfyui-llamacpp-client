# Example configurations for different use cases

## Basic Text Completion
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "completion",
  "prompt": "Explain machine learning in simple terms:",
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "n_predict": 150,
  "seed": -1
}
```

## Creative Writing with Advanced Sampling
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "completion",
  "prompt": "Write a short story about a time traveler:",
  "temperature": 0.9,
  "top_p": 0.95,
  "min_p": 0.05,
  "dynatemp_range": 0.3,
  "dynatemp_exponent": 1.2,
  "dry_multiplier": 0.8,
  "dry_base": 1.75,
  "dry_allowed_length": 2,
  "repeat_penalty": 1.05,
  "repeat_last_n": 256,
  "n_predict": 500
}
```

## Chat Conversation
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "chat_completions",
  "system_message": "You are a helpful AI assistant specialized in programming.",
  "user_message": "How do I implement a binary search algorithm in Python?",
  "temperature": 0.3,
  "max_tokens": 200,
  "top_p": 0.9
}
```

## Code Completion with Infill
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "infill",
  "input_prefix": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    ",
  "input_suffix": "\n    return quicksort(left) + middle + quicksort(right)",
  "temperature": 0.2,
  "top_p": 0.8,
  "n_predict": 100
}
```

## JSON Structured Output
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "completion",
  "prompt": "Generate a product review for a laptop:",
  "json_schema": "{\"type\": \"object\", \"properties\": {\"rating\": {\"type\": \"integer\", \"minimum\": 1, \"maximum\": 5}, \"title\": {\"type\": \"string\"}, \"pros\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}}, \"cons\": {\"type\": \"array\", \"items\": {\"type\": \"string\"}}, \"summary\": {\"type\": \"string\"}}, \"required\": [\"rating\", \"title\", \"summary\"]}",
  "temperature": 0.7,
  "n_predict": 300
}
```

## Document Reranking
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "reranking",
  "query": "artificial intelligence machine learning",
  "documents": "[\"Introduction to Neural Networks\", \"Cooking with Python\", \"Deep Learning Fundamentals\", \"JavaScript for Beginners\", \"AI Ethics and Society\", \"Database Design Principles\"]",
  "top_n": 3
}
```

## Text Embeddings
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "embeddings",
  "input_text": "The quick brown fox jumps over the lazy dog.",
  "encoding_format": "float",
  "embd_normalize": 2
}
```

## Tokenization
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "tokenize",
  "content": "Hello, world! How are you today?",
  "add_special": true,
  "with_pieces": true
}
```

## Advanced Chat with Function Calling
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "chat_completions",
  "system_message": "You are a helpful assistant that can search for information and perform calculations.",
  "user_message": "What's the weather like in Tokyo today?",
  "tools": "[{\"type\": \"function\", \"function\": {\"name\": \"get_weather\", \"description\": \"Get current weather information for a location\", \"parameters\": {\"type\": \"object\", \"properties\": {\"location\": {\"type\": \"string\", \"description\": \"The city and country\"}}, \"required\": [\"location\"]}}}]",
  "tool_choice": "auto",
  "temperature": 0.7
}
```

## High-Quality Creative Writing with All Advanced Features
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "completion",
  "prompt": "Write an engaging opening paragraph for a science fiction novel:",
  "temperature": 1.0,
  "dynatemp_range": 0.4,
  "dynatemp_exponent": 1.5,
  "top_k": 60,
  "top_p": 0.92,
  "min_p": 0.02,
  "xtc_probability": 0.1,
  "xtc_threshold": 0.1,
  "typical_p": 0.95,
  "dry_multiplier": 0.8,
  "dry_base": 1.75,
  "dry_allowed_length": 2,
  "dry_penalty_last_n": 512,
  "dry_sequence_breakers": "[\"\\n\", \".\", \"!\", \"?\", \":\"]",
  "repeat_penalty": 1.02,
  "repeat_last_n": 128,
  "presence_penalty": 0.1,
  "frequency_penalty": 0.1,
  "samplers": "[\"dry\", \"top_k\", \"xtc\", \"typ_p\", \"top_p\", \"min_p\", \"temperature\"]",
  "n_predict": 200,
  "n_probs": 5,
  "return_tokens": true,
  "cache_prompt": true
}
```

## LoRA Adapter Configuration
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "completion",
  "prompt": "Translate this text to French: 'The weather is beautiful today.'",
  "lora": "[{\"id\": 0, \"scale\": 0.8}, {\"id\": 1, \"scale\": 0.3}]",
  "temperature": 0.3,
  "n_predict": 50
}
```

## Multimodal Vision with Image
```json
{
  "server_url": "http://127.0.0.1:8080",
  "endpoint": "completion",
  "prompt": "Describe what you see in this image: [img-1]",
  "image_data": "[{\"data\": \"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==\", \"id\": 1}]",
  "temperature": 0.7,
  "n_predict": 100
}
```

Note: Replace the base64 image data with actual image data when using multimodal features.
