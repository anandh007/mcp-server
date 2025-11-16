import pytest
from app.exchange_client import ExchangeClient
import asyncio

@pytest.mark.asyncio
async def test_fetch_ticker_binance():
    client = ExchangeClient("binance")
    ticker = await client.fetch_ticker("BTC/USDT")
    assert isinstance(ticker, dict)
    await client.close()
