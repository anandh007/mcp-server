🚀 MCP Server – Crypto Market Data Platform
............................................
A FastAPI-based crypto pricing, OHLCV data, and WebSocket live updates server.

📌 Overview
.............
MCP Server is a lightweight crypto market data backend built using FastAPI, Redis, and CCXT.
It supports:
Live ticker data
OHLCV (candlestick) data
WebSocket real-time updates
Redis caching for high performance
Fully tested using pytest (all tests passing)

🔧 Tech Stack
.............
Python 3.11
FastAPI
CCXT (Async support)
Redis
pytest
WebSockets

📂 Project Structure
.....................
mcp-server/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── exchange_client.py
│   ├── broadcaster.py
│   ├── cache.py
│   ├── config.py
│
├── tests/
├── README.md
└── requirements.txt

▶️ Running the Project
........................

1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Start Redis
redis-server

3️⃣ Run FastAPI Server
uvicorn app.main:app --reload

🧪 Running Tests
..................

All tests must pass (10 passed ✔️):
pytest -q

📡 API Endpoints
.................
✅ Health Check
GET /api/health

📈 Get Crypto Ticker
GET /api/ticker?exchange=binance&symbol=BTC/USDT

🕯️ Get OHLCV Candles
GET /api/ohlcv?exchange=binance&symbol=BTC/USDT&timeframe=1h&limit=5

🔌 WebSocket Live Data
/api/ws

📝 Features
................

1)Real-time market data broadcasting
2)Rate-limited exchange calls
3)Automatic caching using Redis
4)Graceful WebSocket connection handling
5)Fully async architecture
6)10 passing unit tests using pytest
7)Easy to deploy & lightweight backend






