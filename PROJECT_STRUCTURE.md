# 📂 Project Structure

```
realtimestockmarkets_chatbot/
├── src/                      # Source code
│   ├── __init__.py
│   ├── agent.py             # Core agent with LLM & tools
│   ├── api.py               # FastAPI server (port 8000)
│   └── app.py               # Streamlit interface (port 8501)
│
├── tests/                    # Test files
│   ├── __init__.py
│   ├── test_agent.py        # Agent function tests
│   └── test_api.py          # API endpoint tests
│
├── data/                     # Database and logs
│   └── agent_logs.db        # SQLite logs (auto-created)
│
├── .env                      # Environment configuration (not in git)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── README.md                # Main documentation
├── API_EXAMPLES.md          # API usage examples
├── start_api.sh            # Start API server
└── start_streamlit.sh      # Start Streamlit app
```

## 📁 Directory Details

### `src/` - Source Code
Contains all application code:
- **`agent.py`** - Core AI agent with stock market tools and math operations
- **`api.py`** - REST API backend using FastAPI
- **`app.py`** - Web chat interface using Streamlit

### `tests/` - Tests
Contains all test files:
- **`test_agent.py`** - Tests for agent functions (stock data, calculations)
- **`test_api.py`** - Tests for API endpoints

### `data/` - Database & Logs
Stores application data:
- **`agent_logs.db`** - SQLite database with conversation logs
  - Automatically created on first run
  - Contains: prompts, responses, tokens, latency, tool calls
  - Ignored by git (see `.gitignore`)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API credentials
```

### 3. Run Application

**Streamlit Chat Interface:**
```bash
./start_streamlit.sh
# Opens at http://localhost:8501
```

**FastAPI Server:**
```bash
./start_api.sh
# Opens at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## 🧪 Running Tests

**Test Agent Functions:**
```bash
python tests/test_agent.py
```

**Test API Endpoints:**
```bash
# First start the API server, then:
python tests/test_api.py
```

## 📊 Database

All interactions are logged to `data/agent_logs.db`:

**View recent logs:**
```bash
sqlite3 data/agent_logs.db "SELECT timestamp, prompt, response FROM logs ORDER BY timestamp DESC LIMIT 5;"
```

**View token usage:**
```bash
sqlite3 data/agent_logs.db "SELECT SUM(total_tokens) as total FROM logs;"
```

## 🔧 Development

**Project uses modular imports:**
```python
from src.agent import chat, init_db
from src.api import app
```

**Add new tools to agent:**
1. Define function in `src/agent.py`
2. Add to `TOOLS` list
3. Add to `AVAILABLE_FUNCTIONS` dict

## 📝 Notes

- Database (`data/`) is excluded from git
- Logs persist between runs
- All modules are in `src/` for clean organization
- Tests are separate in `tests/` directory
