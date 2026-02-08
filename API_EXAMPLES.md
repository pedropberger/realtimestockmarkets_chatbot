# API Usage Examples

## Start the API Server

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Example Requests

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy"
}
```

### 2. Get Example Queries

```bash
curl http://localhost:8000/examples
```

### 3. Get Stock Symbols Reference

```bash
curl http://localhost:8000/symbols
```

### 4. Simple Chat Request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the current price of Apple stock?"
  }'
```

Response:
```json
{
  "response": "The current price of Apple stock (AAPL) is $278.12.",
  "tokens_input": 245,
  "tokens_output": 28,
  "total_tokens": 273,
  "latency_ms": 1523,
  "tool_calls": [
    {
      "function": "get_current_price",
      "arguments": {"symbol": "AAPL"}
    }
  ]
}
```

### 5. Chat with Conversation History

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "And what about Tesla?",
    "conversation_history": [
      {
        "role": "user",
        "content": "What is the current price of Apple?"
      },
      {
        "role": "assistant",
        "content": "The current price of Apple stock is $278.12."
      }
    ]
  }'
```

### 6. Mathematical Calculation

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate 250 * 3.5 + 100"
  }'
```

### 7. Stock Price History

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What was Bitcoin price yesterday?"
  }'
```

### 8. Price Change Percentage

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What percentage did Tesla stock change compared to yesterday?"
  }'
```

### 9. Average Price Over Time

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Calculate the average stock price of Microsoft over the last week"
  }'
```

## Python Client Example

```python
import requests

# Simple request
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "What's the current price of Tesla?"}
)

result = response.json()
print(f"Response: {result['response']}")
print(f"Latency: {result['latency_ms']}ms")
```

## JavaScript/Fetch Example

```javascript
fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: "What's the current price of Apple?"
  })
})
.then(response => response.json())
.then(data => {
  console.log('Response:', data.response);
  console.log('Tokens:', data.total_tokens);
  console.log('Latency:', data.latency_ms + 'ms');
});
```

## Database Logs

All chat interactions are automatically logged to `agent_logs.db` with:
- Timestamp
- User prompt
- AI response
- Model name
- Token usage (input/output/total)
- Latency in milliseconds
- Tool calls executed

You can query the database:

```bash
sqlite3 agent_logs.db "SELECT timestamp, prompt, response, total_tokens, latency_ms FROM logs ORDER BY timestamp DESC LIMIT 5;"
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `500`: Internal server error

Error response format:
```json
{
  "detail": "Error message here"
}
```
