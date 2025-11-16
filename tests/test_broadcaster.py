import pytest
from app.broadcaster import Broadcaster

class DummyWS:
    def __init__(self):
        self.sent = []

    async def send_json(self, data):
        self.sent.append(data)


@pytest.mark.asyncio
async def test_broadcaster_register_unregister():
    bc = Broadcaster()
    ws = DummyWS()

    await bc.register(ws)
    assert ws in bc.clients

    await bc.unregister(ws)
    assert ws not in bc.clients
