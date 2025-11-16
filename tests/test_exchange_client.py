import pytest
from app.exchange_client import ExchangeClient

@pytest.mark.asyncio
async def test_exchange_client_valid():
    client = ExchangeClient("binance")
    ticker = await client.fetch_ticker("BTC/USDT")
    assert "last" in ticker
    await client.close()

@pytest.mark.asyncio
async def test_exchange_client_invalid_exchange():
    with pytest.raises(ValueError):
        ExchangeClient("invalid_exchange")

@pytest.mark.asyncio
async def test_exchange_client_invalid_symbol():
    client = ExchangeClient("binance")
    with pytest.raises(Exception):
        await client.fetch_ticker("FAKE/PAIR")
    await client.close()
