# Changelog

All notable changes to the ComfyUI Llama.cpp Client Node will be documented in this file.

## [1.0.0] - 2025-08-05

### Added
- Initial release of ComfyUI Llama.cpp Client Node
- Complete support for all llama-server endpoints:
  - `/completion` - Text completion with full parameter support
  - `/v1/chat/completions` - OpenAI-compatible chat API
  - `/v1/embeddings` - Text embeddings generation
  - `/tokenize` - Text tokenization
  - `/detokenize` - Token to text conversion
  - `/apply-template` - Chat template formatting
  - `/infill` - Code completion and infilling
  - `/v1/rerank` - Document reranking

### Core Features
- **Advanced Sampling**: Full support for all sampling methods
  - Temperature, top-k, top-p, min-p sampling
  - Dynamic temperature with range and exponent
  - XTC (Cross-Token Coherence) sampling
  - DRY (Don't Repeat Yourself) sampling
  - Mirostat v1 and v2 sampling
  - Locally typical sampling
  - Custom sampler ordering

- **Repetition Control**: Comprehensive repetition management
  - Standard repeat penalty
  - OpenAI-style presence and frequency penalties
  - DRY sampling with configurable breakers
  - Configurable context windows

- **Grammar and Constraints**: Structured output generation
  - BNF grammar support for constrained generation
  - JSON Schema validation for structured output
  - Logit bias for fine-grained token control

- **Multimodal Support**: Vision model integration
  - Base64 image data processing
  - Image reference system for prompts
  - Full multimodal parameter support

- **Function Calling**: Tool use capabilities
  - OpenAI-compatible function calling
  - Tool choice strategies
  - Complex tool definitions

- **Performance Optimization**: Advanced caching and performance features
  - KV cache reuse between requests
  - Slot management for concurrent processing
  - Timing controls and monitoring
  - Response field selection

- **LoRA Support**: Dynamic adapter configuration
  - Per-request LoRA adapter settings
  - Multiple adapter combinations
  - Configurable scaling factors

- **Streaming Support**: Real-time generation
  - Token-by-token streaming
  - Probability information
  - Detailed timing data

### Documentation
- Comprehensive README with usage examples
- Complete parameter reference guide (PARAMETERS.md)
- Example configurations for common use cases (examples.md)
- Test script for validation (test_node.py)

### Technical Features
- **Error Handling**: Robust error management and reporting
- **Type Safety**: Proper parameter validation and conversion
- **JSON Parsing**: Intelligent handling of JSON parameters
- **Connection Management**: Timeout and retry logic
- **Authentication**: API key support

### Output
- Four-output design: response, raw_response, error, status_code
- Flexible response processing
- Detailed error information
- HTTP status code reporting

### Compatibility
- Full llama.cpp server API compatibility
- Support for all model types (text, multimodal, embedding)
- OpenAI API compatibility where applicable
- ComfyUI integration standards compliance

### Files Added
- `__init__.py` - ComfyUI integration
- `llamacpp_client_node.py` - Main node implementation
- `README.md` - User documentation
- `PARAMETERS.md` - Complete parameter reference
- `examples.md` - Usage examples and configurations
- `test_node.py` - Testing and validation script
- `requirements.txt` - Python dependencies
- `CHANGELOG.md` - Version history

### Dependencies
- `requests>=2.25.1` - HTTP client library
- `pillow>=8.0.0` - Image processing for multimodal support

### Known Limitations
- Requires active llama-server instance
- Some features depend on model capabilities
- Large parameter sets may impact UI performance
- Streaming mode requires special handling in ComfyUI workflows

### Future Considerations
- WebSocket support for improved streaming
- Built-in server management
- Model-specific parameter validation
- Performance profiling tools
- Advanced caching strategies

---

## Version Format

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH
- MAJOR: Incompatible API changes
- MINOR: New functionality (backward compatible)
- PATCH: Bug fixes (backward compatible)
