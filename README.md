# Stock Market AI Chatbot

An AI-powered conversational agent that provides real-time stock market information and performs mathematical operations using LLM function calling.

## ✨ Features

- **Real-time Stock Data**: Get current prices, historical data, price changes, and averages via Yahoo Finance
- **Mathematical Operations**: Perform calculations and percentage computations
- **Multiple Interfaces**: 
  - 🎨 Streamlit chat interface with beautiful UI
  - 🚀 FastAPI REST API with interactive documentation
- **Logging**: All interactions logged to SQLite database with comprehensive metrics
- **🐳 Docker Support**: Fully containerized with persistent log storage

## 📋 Prerequisites

- Docker (recommended) or Python 3.11+
- LLM API credentials (OpenAI, Azure OpenAI, Groq, etc.)

## 🚀 Quick Start with Docker

### 1. Configure Environment Variables

Create a `.env` file in the project root:

```env
ENDPOINT=https://api.openai.com/v1
DEPLOYMENT_NAME=gpt-4
API_KEY=your_api_key_here
```

**⚠️ IMPORTANT**: Do **NOT** use quotes around the values!

**Examples for different providers:**

```env
# OpenAI
ENDPOINT=https://api.openai.com/v1
DEPLOYMENT_NAME=gpt-4
API_KEY=sk-...

# Azure OpenAI
ENDPOINT=https://your-resource.openai.azure.com/openai/v1/
DEPLOYMENT_NAME=your-deployment-name
API_KEY=your-azure-key

# Groq
ENDPOINT=https://api.groq.com/openai/v1
DEPLOYMENT_NAME=llama-3.3-70b-versatile
API_KEY=gsk_...
```

### 2. Run the Streamlit App

**Build the image:**
```bash
docker build -t stock-chatbot-streamlit .
```

**Run the container:**

**Linux/Mac:**
```bash
docker run -d -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  --name stock-streamlit \
  stock-chatbot-streamlit
```

**Windows PowerShell:**
```powershell
docker run -d -p 8501:8501 --env-file .env -v ${PWD}/data:/app/data --name stock-streamlit stock-chatbot-streamlit
```

**Windows CMD:**
```cmd
docker run -d -p 8501:8501 --env-file .env -v %cd%/data:/app/data --name stock-streamlit stock-chatbot-streamlit
```

**Access the app:** http://localhost:8501

### 3. Run the API (Optional)

**Build the image:**
```bash
docker build -f Dockerfile.api -t stock-chatbot-api .
```

**Run the container:**

**Linux/Mac:**
```bash
docker run -d -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  --name stock-api \
  stock-chatbot-api
```

**Windows PowerShell:**
```powershell
docker run -d -p 8000:8000 --env-file .env -v ${PWD}/data:/app/data --name stock-api stock-chatbot-api
```

**Windows CMD:**
```cmd
docker run -d -p 8000:8000 --env-file .env -v %cd%/data:/app/data --name stock-api stock-chatbot-api
```

**Access the API:**
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

## 💻 Local Development (without Docker)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file as described above.

### 3. Run Applications

**Streamlit App:**
```bash
streamlit run src/app.py
```

**FastAPI Server:**
```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

**Direct Python Usage:**
```python
from src.agent import simple_chat

response = simple_chat("What's the current price of Tesla?")
print(response)
```

## 📡 API Endpoints

### `POST /chat`
Main chatbot endpoint.

**Request:**
```json
{
  "message": "What's the current price of Tesla?",
  "conversation_history": []
}
```

**Response:**
```json
{
  "response": "The current price of Tesla...",
  "tokens_input": 123,
  "tokens_output": 45,
  "total_tokens": 168,
  "latency_ms": 1234,
  "tool_calls": [...]
}
```

### `GET /health`
Health check endpoint.

### `GET /examples`
Returns example queries the chatbot can handle.

### `GET /symbols`
Returns common stock ticker symbols.

## 🧪 Example Queries

**Stock Information:**
- "What's the current price of Tesla?"
- "What was the Bitcoin price yesterday?"
- "What's the percentage change of Apple compared to yesterday?"
- "Calculate the average stock price of Microsoft over the last week"

**Mathematical Calculations:**
- "Calculate 150 * 2.5 + 100"
- "What's 15% of 1000?"
- "Calculate (500 + 300) / 2"

**Combined:**
- "What's the current price of AAPL and calculate 10% of it?"

## 📈 Stock Symbols

Common symbols you can query:
- **AAPL** - Apple Inc.
- **TSLA** - Tesla Inc.
- **MSFT** - Microsoft Corporation
- **GOOGL** - Alphabet Inc. (Google)
- **BTC-USD** - Bitcoin
- **ETH-USD** - Ethereum

## 📊 Database Logs

All interactions are logged to `data/agent_logs.db` with:
- Timestamp
- Prompt and response
- Model name
- Token counts (input, output, total)
- Latency (ms)
- Tool calls executed

**View logs:**
```bash
sqlite3 data/agent_logs.db "SELECT timestamp, prompt, response FROM logs ORDER BY timestamp DESC LIMIT 5;"
```

---

## 🐳 Additional Docker Information

### Docker Commands Reference

**View logs:**
```bash
# Streamlit
docker logs stock-streamlit

# API
docker logs stock-api

# Follow logs in real-time
docker logs -f stock-streamlit
```

**Stop containers:**
```bash
docker stop stock-streamlit stock-api
```

**Remove containers:**
```bash
docker rm stock-streamlit stock-api
```

**Restart containers:**
```bash
docker restart stock-streamlit stock-api
```

**Debug inside container:**
```bash
docker exec -it stock-streamlit /bin/bash
docker exec -it stock-api /bin/bash
```

### Testing the API with curl

**Health check:**
```bash
curl http://localhost:8000/health
```

**Chat request:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What'\''s 10% of 500?"
  }'
```

**Get examples:**
```bash
curl http://localhost:8000/examples
```

### Testing with Python

```python
import requests

# Chat request
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What's the current price of Tesla?"}
)
print(response.json())

# Get available symbols
symbols = requests.get("http://localhost:8000/symbols")
print(symbols.json())
```

### Development Mode with Hot Reload

For development with automatic code reloading, mount the source code as a volume:

**Streamlit (Linux/Mac):**
```bash
docker run -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/src:/app/src \
  --name stock-streamlit \
  stock-chatbot-streamlit
```

**Streamlit (Windows PowerShell):**
```powershell
docker run -p 8501:8501 --env-file .env -v ${PWD}/data:/app/data -v ${PWD}/src:/app/src --name stock-streamlit stock-chatbot-streamlit
```

**API (Linux/Mac):**
```bash
docker run -p 8000:8000 \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/src:/app/src \
  --name stock-api \
  stock-chatbot-api \
  uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

**API (Windows PowerShell):**
```powershell
docker run -p 8000:8000 --env-file .env -v ${PWD}/data:/app/data -v ${PWD}/src:/app/src --name stock-api stock-chatbot-api uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload
```

### Rebuild After Code Changes

**Linux/Mac:**
```bash
# Streamlit
docker stop stock-streamlit && docker rm stock-streamlit
docker build -t stock-chatbot-streamlit .
docker run -d -p 8501:8501 --env-file .env -v $(pwd)/data:/app/data --name stock-streamlit stock-chatbot-streamlit

# API
docker stop stock-api && docker rm stock-api
docker build -f Dockerfile.api -t stock-chatbot-api .
docker run -d -p 8000:8000 --env-file .env -v $(pwd)/data:/app/data --name stock-api stock-chatbot-api
```

**Windows PowerShell:**
```powershell
# Streamlit
docker stop stock-streamlit; docker rm stock-streamlit
docker build -t stock-chatbot-streamlit .
docker run -d -p 8501:8501 --env-file .env -v ${PWD}/data:/app/data --name stock-streamlit stock-chatbot-streamlit

# API
docker stop stock-api; docker rm stock-api
docker build -f Dockerfile.api -t stock-chatbot-api .
docker run -d -p 8000:8000 --env-file .env -v ${PWD}/data:/app/data --name stock-api stock-chatbot-api
```

## 🔍 Troubleshooting

### Connection Error in App

**Symptom:** "❌ Error: Connection error."

**Cause:** Quotes in environment variable values.

**Solution:** Check your `.env` file - it should NOT have quotes:

```env
# ✅ Correct format:
ENDPOINT=https://your-endpoint.com/v1/
API_KEY=your-key-here

# ❌ Wrong format (includes quotes in actual value):
ENDPOINT="https://your-endpoint.com/v1/"
API_KEY="your-key-here"
```

After fixing, restart the containers:
```bash
docker stop stock-streamlit stock-api
docker rm stock-streamlit stock-api
# Run the containers again
```

### Container Won't Start

```bash
# View error logs
docker logs stock-streamlit
docker logs stock-api

# Check if ports are in use
lsof -i :8501  # Streamlit
lsof -i :8000  # API
```

### Health Check Failing

```bash
# Check health status
docker inspect --format='{{json .State.Health}}' stock-streamlit | jq
docker inspect --format='{{json .State.Health}}' stock-api | jq
```

### Verify Environment Variables

```bash
# Check inside container
docker exec stock-streamlit env | grep -E 'ENDPOINT|API_KEY|DEPLOYMENT_NAME'
docker exec stock-api env | grep -E 'ENDPOINT|API_KEY|DEPLOYMENT_NAME'
```

## 🔐 Security Best Practices

- ⚠️ **NEVER** commit the `.env` file to version control
- ✅ The `.env` file is excluded via `.dockerignore` - it won't be copied into the Docker image
- ✅ Environment variables are injected at runtime via `--env-file`
- ✅ Use platform secrets (AWS Secrets Manager, Azure Key Vault) for production deployments

## 🌐 Production Deployment

### Uvicorn Workers

For production API deployments, configure multiple workers in `Dockerfile.api`:

```dockerfile
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Cloud Deployment Example

```bash
# Tag images
docker tag stock-chatbot-streamlit:latest your-registry/stock-chatbot-streamlit:v1.0.0
docker tag stock-chatbot-api:latest your-registry/stock-chatbot-api:v1.0.0

# Push to registry
docker push your-registry/stock-chatbot-streamlit:v1.0.0
docker push your-registry/stock-chatbot-api:v1.0.0
```

### Docker Compose (Optional)

Create a `docker-compose.yml` to orchestrate both services:

```yaml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  streamlit:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    depends_on:
      - api
    restart: unless-stopped
```

Then run:
```bash
docker-compose up -d
```

## 📦 Image Information

**View image sizes:**
```bash
docker images stock-chatbot-streamlit
docker images stock-chatbot-api
```

**View image layers:**
```bash
docker history stock-chatbot-streamlit
docker history stock-chatbot-api
```

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.