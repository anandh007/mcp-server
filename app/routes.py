from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from .exchange_client import ExchangeClient
from .cache import get_cached, set_cached
from .config import settings
import json
from datetime import datetime


def to_datetime(ms_timestamp: int):
    """Convert milliseconds timestamp → human readable."""
    try:
        return datetime.utcfromtimestamp(ms_timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return None


router = APIRouter()
router.broadcaster = None  # will be injected by main.py


# ---------------------------
# Health Endpoint
# ---------------------------
@router.get("/health")
async def health():
    return {"status": "ok"}


# ---------------------------
# Ticker Endpoint (TEST FIXED)
# ---------------------------
@router.get("/ticker")
async def get_ticker(exchange: str, symbol: str):
    cache_key = f"ticker:{exchange}:{symbol}"
    cached = await get_cached(cache_key)

    if cached:
        return json.loads(cached)

    client = ExchangeClient(exchange)
    ticker = await client.fetch_ticker(symbol)
    await client.close()

    # THIS SHAPE IS REQUIRED BY TESTS
    payload = {
        "data": {
            "last": ticker.get("last"),
            "high": ticker.get("high"),
            "low": ticker.get("low"),
            "percentage": ticker.get("percentage"),
        }
    }

    await set_cached(cache_key, json.dumps(payload), ttl=10)
    return payload



# ---------------------------
# WebSocket Endpoint
# ---------------------------
@router.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):

    print("📥 WS REQUEST RECEIVED")

    broadcaster = router.broadcaster

    if broadcaster is None:
        print("❌ broadcaster is STILL None - not injected")
        await websocket.close()
        return

    await websocket.accept()
    print("🔌 WebSocket ACCEPTED")

    await broadcaster.register(websocket)
    print("📡 Client REGISTERED to broadcaster")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("❌ Client DISCONNECTED")
        await broadcaster.unregister(websocket)


# ---------------------------
# OHLCV Endpoint (TEST FIXED)
# ---------------------------
@router.get("/ohlcv")
async def get_ohlcv(exchange: str, symbol: str, timeframe: str = "1h", limit: int = 5):
    client = ExchangeClient(exchange)
    raw = await client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    await client.close()

    if not raw or len(raw) == 0:
        # Tests expect at least 1 candle
        raise HTTPException(status_code=500, detail="OHLCV empty")

    candles = []
    for c in raw:
        candles.append({
            "open": c[1],
            "high": c[2],
            "low": c[3],
            "close": c[4],
            "volume": c[5]
        })

    return {"candles": candles}


