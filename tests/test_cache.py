import pytest
from app.cache import set_cached, get_cached

@pytest.mark.asyncio
async def test_cache_set_and_get():
    await set_cached("test:key", "123", ttl=5)
    val = await get_cached("test:key")
    assert val == "123"
