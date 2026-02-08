#!/usr/bin/env python3
"""
Test script for agent.py functions
"""

from agent import (
    init_db,
    get_current_price,
    get_historical_price,
    get_price_change,
    get_average_price,
    calculate,
    percentage_calculation,
    simple_chat
)

def test_stock_functions():
    """Test stock market functions"""
    print("=" * 50)
    print("Testing Stock Market Functions")
    print("=" * 50)
    
    # Test current price
    print("\n1. Testing get_current_price for AAPL:")
    result = get_current_price("AAPL")
    print(result)
    
    # Test historical price
    print("\n2. Testing get_historical_price for TSLA (2024-01-15):")
    result = get_historical_price("TSLA", "2024-01-15")
    print(result)
    
    # Test price change
    print("\n3. Testing get_price_change for BTC-USD:")
    result = get_price_change("BTC-USD", days=1)
    print(result)
    
    # Test average price
    print("\n4. Testing get_average_price for MSFT (7 days):")
    result = get_average_price("MSFT", days=7)
    print(result)


def test_math_functions():
    """Test mathematical functions"""
    print("\n" + "=" * 50)
    print("Testing Mathematical Functions")
    print("=" * 50)
    
    # Test calculation
    print("\n1. Testing calculate:")
    result = calculate("150 * 2.5 + 100")
    print(result)
    
    # Test percentage
    print("\n2. Testing percentage_calculation:")
    result = percentage_calculation(1000, 15)
    print(result)


def test_chat_function():
    """Test the main chat function"""
    print("\n" + "=" * 50)
    print("Testing Chat Function")
    print("=" * 50)
    
    print("\n1. Testing simple stock query:")
    response = simple_chat("What's the current price of Apple stock?")
    print(f"Response: {response}")
    
    print("\n2. Testing calculation:")
    response = simple_chat("Can you calculate 250 * 3.5?")
    print(f"Response: {response}")


if __name__ == "__main__":
    # Initialize database
    print("Initializing database...")
    init_db()
    print("Database initialized!\n")
    
    # Run tests
    test_stock_functions()
    test_math_functions()
    
    # Uncomment to test chat with real LLM (requires API key)
    # test_chat_function()
    
    print("\n" + "=" * 50)
    print("Tests completed!")
    print("=" * 50)
