from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from agent import chat, init_db

# Initialize database on startup
init_db()

# Create FastAPI app
app = FastAPI(
    title="Stock Market AI Chatbot API",
    description="AI agent for real-time stock market information and mathematical operations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = None


class ChatResponse(BaseModel):
    response: str
    tokens_input: Optional[int] = None
    tokens_output: Optional[int] = None
    total_tokens: Optional[int] = None
    latency_ms: Optional[int] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None


# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Stock Market AI Chatbot API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Main chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint that processes user messages and returns AI responses.
    
    Args:
        request: ChatRequest containing user message and optional conversation history
        
    Returns:
        ChatResponse with AI response and metadata
    """
    try:
        # Build messages list
        messages = []
        
        # Add conversation history if provided
        if request.conversation_history:
            messages.extend([
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ])
        
        # Add current user message
        messages.append({"role": "user", "content": request.message})
        
        # Get response from agent
        result = chat(messages)
        
        # Check for errors
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Return response
        return ChatResponse(
            response=result.get("response", ""),
            tokens_input=result.get("tokens_input"),
            tokens_output=result.get("tokens_output"),
            total_tokens=result.get("total_tokens"),
            latency_ms=result.get("latency_ms"),
            tool_calls=result.get("tool_calls")
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Example queries endpoint
@app.get("/examples")
async def get_examples():
    """Get example queries that the chatbot can handle"""
    return {
        "stock_queries": [
            "What's the current price of Tesla?",
            "What was the Bitcoin price yesterday?",
            "What's the percentage change of Apple compared to yesterday?",
            "Can you calculate the average stock price of Microsoft over the last week?"
        ],
        "math_queries": [
            "Calculate 150 * 2.5 + 100",
            "What's 15% of 1000?",
            "Calculate (500 + 300) / 2"
        ],
        "combined_queries": [
            "What's the current price of AAPL and calculate 10% of it?",
            "Compare Tesla's price change to Apple's price change"
        ]
    }


# Stock symbols reference endpoint
@app.get("/symbols")
async def get_symbols():
    """Get common stock symbols"""
    return {
        "stocks": {
            "AAPL": "Apple Inc.",
            "TSLA": "Tesla Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc. (Google)",
            "AMZN": "Amazon.com Inc.",
            "META": "Meta Platforms Inc.",
            "NVDA": "NVIDIA Corporation",
            "AMD": "Advanced Micro Devices Inc."
        },
        "crypto": {
            "BTC-USD": "Bitcoin",
            "ETH-USD": "Ethereum",
            "SOL-USD": "Solana"
        },
        "indices": {
            "^GSPC": "S&P 500",
            "^DJI": "Dow Jones Industrial Average",
            "^IXIC": "NASDAQ Composite"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
