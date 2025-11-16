import pytest

@pytest.mark.asyncio
async def test_ohlcv(client):
    res = await client.get(
        "/api/ohlcv?exchange=binance&symbol=BTC/USDT&timeframe=1h&limit=5"
    )

    assert res.status_code == 200
    payload = res.json()
    assert "candles" in payload
    assert len(payload["candles"]) > 0

    candle = payload["candles"][0]
    for f in ["open", "high", "low", "close", "volume"]:
        assert f in candle
