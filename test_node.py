#!/usr/bin/env python3
"""
Test script for the LlamaCpp Client Node
Run this to verify the node works correctly before using in ComfyUI
"""

import sys
import json
from llamacpp_client_node import LlamaCppClientNode

def test_node():
    """Test the LlamaCpp Client Node with various endpoints."""
    
    print("Testing LlamaCpp Client Node...")
    print("=" * 50)
    
    # Initialize the node
    node = LlamaCppClientNode()
    
    # Test server URL (modify as needed)
    server_url = "http://127.0.0.1:8080"
    
    # Test 1: Basic completion
    print("\n1. Testing basic completion...")
    try:
        response, raw_response, error, status_code = node.process_request(
            server_url=server_url,
            endpoint="completion",
            prompt="Hello, how are you?",
            temperature=0.7,
            n_predict=20
        )
        
        if error or status_code >= 400:
            print(f"❌ Error: {error or 'HTTP Error'} (Status: {status_code})")
            if raw_response:
                print(f"Raw response: {raw_response[:200]}...")
        else:
            print(f"✅ Success! Status: {status_code}")
            if isinstance(response, dict):
                print(f"Response preview: {str(response)[:100]}...")
            else:
                print(f"Response preview: {response[:100]}...")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 2: Chat completions
    print("\n2. Testing chat completions...")
    try:
        response, raw_response, error, status_code = node.process_request(
            server_url=server_url,
            endpoint="chat_completions",
            prompt="",  # Empty prompt as it's not used for chat_completions
            system_message="You are a helpful assistant.",
            user_message="What is 2+2?",
            temperature=0.3,
            max_tokens=50
        )
        
        if error or status_code >= 400:
            print(f"❌ Error: {error or 'HTTP Error'} (Status: {status_code})")
            if raw_response:
                print(f"Raw response: {raw_response[:200]}...")
        else:
            print(f"✅ Success! Status: {status_code}")
            try:
                parsed = json.loads(raw_response)
                if 'choices' in parsed and len(parsed['choices']) > 0:
                    content = parsed['choices'][0].get('message', {}).get('content', 'No content')
                    print(f"Chat response: {content}")
                else:
                    print(f"No choices in response: {parsed}")
            except:
                if isinstance(response, dict):
                    print(f"Response preview: {str(response)[:100]}...")
                else:
                    print(f"Response preview: {response[:100]}...")
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 3: Tokenization
    print("\n3. Testing tokenization...")
    try:
        response, raw_response, error, status_code = node.process_request(
            server_url=server_url,
            endpoint="tokenize",
            prompt="",  # Empty prompt as we use content parameter
            content="Hello world!",
            with_pieces=True
        )
        
        if error or status_code >= 400:
            print(f"❌ Error: {error or 'HTTP Error'} (Status: {status_code})")
            if raw_response:
                print(f"Raw response: {raw_response[:200]}...")
        else:
            print(f"✅ Success! Status: {status_code}")
            try:
                parsed = json.loads(raw_response)
                if 'tokens' in parsed:
                    print(f"Tokens: {parsed['tokens'][:5]}...")  # First 5 tokens
            except:
                if isinstance(response, dict):
                    print(f"Response preview: {str(response)[:100]}...")
                else:
                    print(f"Response preview: {response[:100]}...")
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    # Test 4: Advanced sampling
    print("\n4. Testing advanced sampling parameters...")
    try:
        response, raw_response, error, status_code = node.process_request(
            server_url=server_url,
            endpoint="completion",
            prompt="Write a creative sentence:",
            temperature=0.9,
            top_k=40,
            top_p=0.9,
            min_p=0.05,
            dynatemp_range=0.2,
            dry_multiplier=0.8,
            mirostat=0,
            repeat_penalty=1.1,
            n_predict=30
        )
        
        if error or status_code >= 400:
            print(f"❌ Error: {error or 'HTTP Error'} (Status: {status_code})")
            if raw_response:
                print(f"Raw response: {raw_response[:200]}...")
        else:
            print(f"✅ Success! Status: {status_code}")
            if isinstance(response, dict):
                print(f"Creative response: {str(response)[:100]}...")
            else:
                print(f"Creative response: {response[:100]}...")
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    
    print("\n" + "=" * 50)
    print("Testing completed!")
    print("\nNote: Some tests may fail if:")
    print("- llama-server is not running")
    print("- Server URL is incorrect")
    print("- Specific endpoints are not enabled")
    print("- Model doesn't support certain features")

if __name__ == "__main__":
    test_node()
