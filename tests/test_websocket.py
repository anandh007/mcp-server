import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_websocket_connect():
    with client.websocket_connect("/api/ws") as ws:
        ws.send_text("ping")
        # Server ignores input but keeps connection alive
