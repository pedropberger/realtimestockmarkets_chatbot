#!/usr/bin/env python3
"""
Test script for API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test health check endpoint"""
    print("=" * 50)
    print("Testing Health Check")
    print("=" * 50)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_root():
    """Test root endpoint"""
    print("=" * 50)
    print("Testing Root Endpoint")
    print("=" * 50)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_examples():
    """Test examples endpoint"""
    print("=" * 50)
    print("Testing Examples Endpoint")
    print("=" * 50)
    response = requests.get(f"{BASE_URL}/examples")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_symbols():
    """Test symbols endpoint"""
    print("=" * 50)
    print("Testing Symbols Endpoint")
    print("=" * 50)
    response = requests.get(f"{BASE_URL}/symbols")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_chat_simple():
    """Test simple chat request"""
    print("=" * 50)
    print("Testing Simple Chat")
    print("=" * 50)
    
    payload = {
        "message": "What's the current price of Apple stock?"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Request: {payload['message']}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse: {data['response']}")
        print(f"Tokens - Input: {data['tokens_input']}, Output: {data['tokens_output']}, Total: {data['total_tokens']}")
        print(f"Latency: {data['latency_ms']}ms")
        if data['tool_calls']:
            print(f"Tool Calls: {json.dumps(data['tool_calls'], indent=2)}")
    else:
        print(f"Error: {response.text}")
    print()


def test_chat_with_history():
    """Test chat with conversation history"""
    print("=" * 50)
    print("Testing Chat with History")
    print("=" * 50)
    
    payload = {
        "message": "And what about Tesla?",
        "conversation_history": [
            {
                "role": "user",
                "content": "What's the current price of Apple?"
            },
            {
                "role": "assistant",
                "content": "The current price of Apple stock (AAPL) is $278.12."
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Request: {payload['message']}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse: {data['response']}")
        print(f"Latency: {data['latency_ms']}ms")
    else:
        print(f"Error: {response.text}")
    print()


def test_chat_calculation():
    """Test chat with calculation"""
    print("=" * 50)
    print("Testing Chat with Calculation")
    print("=" * 50)
    
    payload = {
        "message": "Calculate 250 * 3.5 + 100"
    }
    
    response = requests.post(f"{BASE_URL}/chat", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Request: {payload['message']}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse: {data['response']}")
        print(f"Latency: {data['latency_ms']}ms")
    else:
        print(f"Error: {response.text}")
    print()


if __name__ == "__main__":
    print("Make sure the API is running on http://localhost:8000")
    print("Start it with: uvicorn api:app --port 8000 --reload\n")
    
    try:
        # Test non-chat endpoints first
        test_health_check()
        test_root()
        test_examples()
        test_symbols()
        
        # Test chat endpoints (these require API key to be configured)
        print("\n" + "=" * 50)
        print("CHAT ENDPOINT TESTS")
        print("(Requires valid API key in .env file)")
        print("=" * 50 + "\n")
        
        # Uncomment these to test chat functionality
        # test_chat_simple()
        # test_chat_with_history()
        # test_chat_calculation()
        
        print("Basic tests completed!")
        print("\nTo test chat endpoints, uncomment the test functions in test_api.py")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("Make sure the API is running with: uvicorn api:app --port 8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
