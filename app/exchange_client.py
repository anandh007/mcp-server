import ccxt.async_support as ccxt
import asyncio
import json
from typing import Dict, Any
from .config import settings
import time
import httpx

class ExchangeClient:
    def __init__(self, exchange_name: str):
        if exchange_name not in settings.exchanges:
            raise ValueError(f"Exchange {exchange_name} not configured")
        self.name = exchange_name
        self.exchange = getattr(ccxt, exchange_name)()
        self.lock = asyncio.Lock()

    async def fetch_ticker(self, symbol: str) -> Dict[str, Any]:
        """Fetch current ticker/prices with basic retry logic."""
        attempts = 3
        delay = 0.5
        for attempt in range(attempts):
            try:
                async with self.lock:
                    ticker = await self.exchange.fetch_ticker(symbol)
                # normalize to JSON-safe
                return json.loads(json.dumps(ticker, default=str))
            except Exception as e:
                if attempt+1 == attempts:
                    raise
                await asyncio.sleep(delay * (attempt+1))
        raise RuntimeError("Unreachable")

    async def fetch_ohlcv(self, symbol: str, timeframe: str = '1m', since: int | None = None, limit: int = 100):
        """Historical candles (ohlcv)"""
        attempts = 3
        for attempt in range(attempts):
            try:
                async with self.lock:
                    data = await self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
                return data
            except Exception:
                await asyncio.sleep(0.5 * (attempt+1))
        # fallback to CoinMarketCap if configured
        if settings.cmc_api_key:
            return await self._fetch_from_cmc(symbol, limit)
        raise

    async def _fetch_from_cmc(self, symbol: str, limit: int):
        # Very basic fallback - CoinMarketCap requires symbol->id mapping; user should configure
        async with httpx.AsyncClient() as client:
            headers = {"X-CMC_PRO_API_KEY": settings.cmc_api_key}
            # This is a placeholder; in production handle proper mapping and endpoints
            r = await client.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest", headers=headers, params={"limit": limit})
            r.raise_for_status()
            return r.json()

    async def close(self):
        await self.exchange.close()
