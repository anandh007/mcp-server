import pytest

@pytest.mark.asyncio
async def test_ticker_live_fetch(client):
    res = await client.get("/api/ticker?exchange=binance&symbol=BTC/USDT")
    assert res.status_code == 200
    
    data = res.json()
    assert "data" in data
    assert "last" in data["data"]
