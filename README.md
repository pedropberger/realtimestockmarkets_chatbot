# Stock Market AI Chatbot

An AI-powered conversational agent that provides real-time stock market information and performs mathematical operations.

## Features

- **Real-time Stock Data**: Get current prices, historical data, price changes, and averages
- **Mathematical Operations**: Perform calculations and percentage computations
- **Multiple Interfaces**: 
  - Streamlit chat interface
  - REST API endpoint
- **Logging**: All interactions logged to SQLite database with metrics

## Setup

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment variables**:
Create a `.env` file with:
```env
ENDPOINT=https://api.groq.com/openai/v1
DEPLOYMENT_NAME=llama-3.3-70b-versatile
API_KEY=your_api_key_here
```

For OpenAI:
```env
ENDPOINT=https://api.openai.com/v1
DEPLOYMENT_NAME=gpt-4
API_KEY=your_openai_api_key
```

3. **Initialize database**:
```python
from agent import init_db
init_db()
```

## Usage

### Streamlit App
```bash
streamlit run app.py
```

### FastAPI Server
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

### Direct Python Usage
```python
from agent import simple_chat

response = simple_chat("What's the current price of Tesla?")
print(response)
```

## Example Queries

- "What was the Bitcoin price yesterday?"
- "What's the current price of Tesla?"
- "What's the percentage change of Apple compared to yesterday?"
- "Can you calculate the average stock price of Microsoft over the last week?"
- "Calculate 150 * 2.5 + 100"

## Stock Symbols

- Apple: AAPL
- Tesla: TSLA
- Microsoft: MSFT
- Bitcoin: BTC-USD
- Google: GOOGL

## Docker

Build and run with Docker:
```bash
docker build -t stock-chatbot .
docker run -p 8501:8501 -p 8000:8000 stock-chatbot
```

## Database Logs

All interactions are logged to `agent_logs.db` with:
- Timestamp
- Prompt and response
- Model name
- Token counts (input, output, total)
- Latency (ms)
- Tool calls executed