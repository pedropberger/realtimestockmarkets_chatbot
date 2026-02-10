import os
import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
import yfinance as yf
import time

# Load environment variables
load_dotenv()

# Initialize OpenAI client
endpoint = os.getenv("ENDPOINT")
deployment_name = os.getenv("DEPLOYMENT_NAME")
api_key = os.getenv("API_KEY")
# Optional: Temperature parameter (some models don't support it)
temperature = os.getenv("TEMPERATURE", None)
if temperature:
    temperature = float(temperature)

client = OpenAI(
    base_url=endpoint,
    api_key=api_key
)


# ===========================
# Database Functions
# ===========================

def init_db():
    """Initialize SQLite database for logging."""
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect("data/agent_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            prompt TEXT NOT NULL,
            model TEXT NOT NULL,
            tokens_input INTEGER,
            tokens_output INTEGER,
            total_tokens INTEGER,
            latency_ms INTEGER,
            response TEXT NOT NULL,
            tool_calls TEXT
        )
    """)
    conn.commit()
    conn.close()


def log_to_db(prompt: str, model: str, tokens_input: int, tokens_output: int, 
              total_tokens: int, latency_ms: int, response: str, tool_calls: Optional[str] = None):
    """Log interaction to SQLite database."""
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect("data/agent_logs.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, prompt, model, tokens_input, tokens_output, 
                         total_tokens, latency_ms, response, tool_calls)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        prompt,
        model,
        tokens_input,
        tokens_output,
        total_tokens,
        latency_ms,
        response,
        tool_calls
    ))
    conn.commit()
    conn.close()


# ===========================
# Stock Market Tools
# ===========================

def get_current_price(symbol: str) -> Dict[str, Any]:
    """Get current stock price for a given symbol."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        
        if data.empty:
            return {"error": f"No data found for symbol {symbol}"}
        
        current_price = data['Close'].iloc[-1]
        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "currency": "USD"
        }
    except Exception as e:
        return {"error": str(e)}


def get_historical_price(symbol: str, date: str) -> Dict[str, Any]:
    """Get historical stock price for a given symbol and date (YYYY-MM-DD)."""
    try:
        ticker = yf.Ticker(symbol)
        # Get data for the specific date plus a buffer
        end_date = datetime.strptime(date, "%Y-%m-%d") + timedelta(days=1)
        start_date = datetime.strptime(date, "%Y-%m-%d") - timedelta(days=5)
        
        data = ticker.history(start=start_date.strftime("%Y-%m-%d"), 
                             end=end_date.strftime("%Y-%m-%d"))
        
        if data.empty:
            return {"error": f"No data found for {symbol} on {date}"}
        
        # Get the closest date to the requested date
        target_data = data[data.index.date == datetime.strptime(date, "%Y-%m-%d").date()]
        
        if target_data.empty:
            # If exact date not found, get the last available date
            target_data = data.iloc[-1]
            actual_date = data.index[-1].strftime("%Y-%m-%d")
            closing_price = round(target_data['Close'], 2)
            return {
                "symbol": symbol,
                "requested_date": date,
                "actual_date": actual_date,
                "closing_price": closing_price,
                "note": f"Exact date not available, showing closest date: {actual_date}"
            }
        
        closing_price = round(target_data['Close'].iloc[0], 2)
        return {
            "symbol": symbol,
            "date": date,
            "closing_price": closing_price
        }
    except Exception as e:
        return {"error": str(e)}


def get_price_change(symbol: str, days: int = 1) -> Dict[str, Any]:
    """Get price change for a symbol over specified number of days."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=f"{days + 5}d")
        
        if len(data) < 2:
            return {"error": f"Insufficient data for {symbol}"}
        
        current_price = data['Close'].iloc[-1]
        previous_price = data['Close'].iloc[-(days + 1)]
        
        price_change = current_price - previous_price
        percentage_change = (price_change / previous_price) * 100
        
        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "previous_price": round(previous_price, 2),
            "price_change": round(price_change, 2),
            "percentage_change": round(percentage_change, 2),
            "days": days
        }
    except Exception as e:
        return {"error": str(e)}


def get_average_price(symbol: str, days: int = 7) -> Dict[str, Any]:
    """Calculate average stock price over specified number of days."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=f"{days + 5}d")
        
        if data.empty:
            return {"error": f"No data found for {symbol}"}
        
        # Get last N days
        recent_data = data.tail(days)
        average_price = recent_data['Close'].mean()
        
        return {
            "symbol": symbol,
            "average_price": round(average_price, 2),
            "days": days,
            "period": f"Last {days} days"
        }
    except Exception as e:
        return {"error": str(e)}


# ===========================
# Mathematical Tools
# ===========================

def calculate(expression: str) -> Dict[str, Any]:
    """Safely evaluate a mathematical expression."""
    try:
        # Only allow safe operations
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}
        
        result = eval(expression)
        return {
            "expression": expression,
            "result": round(result, 2) if isinstance(result, float) else result
        }
    except Exception as e:
        return {"error": str(e)}


def percentage_calculation(value: float, percentage: float) -> Dict[str, Any]:
    """Calculate percentage of a value."""
    try:
        result = (value * percentage) / 100
        return {
            "value": value,
            "percentage": percentage,
            "result": round(result, 2)
        }
    except Exception as e:
        return {"error": str(e)}


# ===========================
# Tool Definitions
# ===========================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_price",
            "description": "Get the current stock price for a given symbol (e.g., AAPL, TSLA, BTC-USD)",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol (e.g., AAPL for Apple, TSLA for Tesla, BTC-USD for Bitcoin)"
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_historical_price",
            "description": "Get historical stock price for a specific date",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol"
                    },
                    "date": {
                        "type": "string",
                        "description": "Date in YYYY-MM-DD format"
                    }
                },
                "required": ["symbol", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_price_change",
            "description": "Get price change and percentage change over a specified period",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to compare (default: 1 for yesterday)",
                        "default": 1
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_average_price",
            "description": "Calculate average stock price over a specified period",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Stock symbol"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days for average calculation (default: 7)",
                        "default": 7
                    }
                },
                "required": ["symbol"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate (e.g., '100 * 2 + 50')"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "percentage_calculation",
            "description": "Calculate percentage of a value",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "number",
                        "description": "The base value"
                    },
                    "percentage": {
                        "type": "number",
                        "description": "The percentage to calculate"
                    }
                },
                "required": ["value", "percentage"]
            }
        }
    }
]


# Map function names to actual functions
AVAILABLE_FUNCTIONS = {
    "get_current_price": get_current_price,
    "get_historical_price": get_historical_price,
    "get_price_change": get_price_change,
    "get_average_price": get_average_price,
    "calculate": calculate,
    "percentage_calculation": percentage_calculation
}


# ===========================
# Agent Chat Function
# ===========================

def chat(messages: List[Dict[str, str]], max_iterations: int = 5) -> Dict[str, Any]:
    """
    Main chat function that handles conversation with tool calling.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        max_iterations: Maximum number of tool calling iterations
    
    Returns:
        Dictionary containing response and metadata
    """
    # Ensure system message exists
    if not messages or messages[0].get("role") != "system":
        system_message = {
            "role": "system",
            "content": """You are a helpful AI assistant that specializes in stock market information and mathematical calculations. 
You have access to real-time stock data and can perform various calculations.

When users ask about stocks:
- Use ticker symbols (AAPL for Apple, TSLA for Tesla, BTC-USD for Bitcoin, etc.)
- Provide clear, concise answers with relevant numbers
- For "yesterday" queries, use the get_historical_price or get_price_change function

Be conversational and helpful. Always provide context with your numbers."""
        }
        messages = [system_message] + messages
    
    start_time = time.time()
    tool_calls_log = []
    
    for iteration in range(max_iterations):
        # Build request parameters
        request_params = {
            "model": deployment_name,
            "messages": messages,
            "tools": TOOLS,
            "tool_choice": "auto"
        }
        
        # Only add temperature if configured (some models don't support it)
        if temperature is not None:
            request_params["temperature"] = temperature
        
        response = client.chat.completions.create(**request_params)
        
        assistant_message = response.choices[0].message
        
        # Check if tool calls are needed
        if not assistant_message.tool_calls:
            # Final response
            end_time = time.time()
            latency_ms = int((end_time - start_time) * 1000)
            
            # Log to database
            log_to_db(
                prompt=messages[-1]["content"] if messages else "",
                model=deployment_name,
                tokens_input=response.usage.prompt_tokens,
                tokens_output=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
                latency_ms=latency_ms,
                response=assistant_message.content,
                tool_calls=json.dumps(tool_calls_log) if tool_calls_log else None
            )
            
            return {
                "response": assistant_message.content,
                "tokens_input": response.usage.prompt_tokens,
                "tokens_output": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "latency_ms": latency_ms,
                "tool_calls": tool_calls_log
            }
        
        # Process tool calls
        messages.append({
            "role": "assistant",
            "content": assistant_message.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in assistant_message.tool_calls
            ]
        })
        
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Log tool call
            tool_calls_log.append({
                "function": function_name,
                "arguments": function_args
            })
            
            # Execute function
            function_to_call = AVAILABLE_FUNCTIONS.get(function_name)
            if function_to_call:
                function_response = function_to_call(**function_args)
            else:
                function_response = {"error": f"Function {function_name} not found"}
            
            # Add function response to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(function_response)
            })
    
    # If max iterations reached
    return {
        "response": "I apologize, but I need more iterations to complete this request.",
        "error": "Max iterations reached"
    }


def simple_chat(user_message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
    """
    Simplified chat function for easy integration.
    
    Args:
        user_message: User's message
        conversation_history: Optional list of previous messages
    
    Returns:
        Assistant's response as string
    """
    if conversation_history is None:
        conversation_history = []
    
    messages = conversation_history + [{"role": "user", "content": user_message}]
    result = chat(messages)
    
    return result.get("response", "Sorry, I couldn't process that request.")