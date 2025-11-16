import asyncio
import json
from .exchange_client import ExchangeClient
from .cache import set_cached
from .config import settings


class Broadcaster:
    def __init__(self):
        self.clients = set()
        self.running = False
        self._task = None

    async def start(self):
        if self.running:
            return

        print("🚀 Broadcaster started")
        self.running = True
        self._task = asyncio.create_task(self._poll_loop())

    async def stop(self):
        print("🛑 Broadcaster stopping...")
        self.running = False

        if self._task:
            self._task.cancel()
            self._task = None

        print("🛑 Broadcaster stopped")

    async def register(self, websocket):
        self.clients.add(websocket)
        print(f"🔌 Client connected – Total: {len(self.clients)}")

    async def unregister(self, websocket):
        if websocket in self.clients:
            self.clients.remove(websocket)
        print(f"❌ Client disconnected – Total: {len(self.clients)}")

    async def _poll_loop(self):
        # Crypto pairs to stream
        pairs = ["BTC/USDT", "ETH/USDT"]
        exchange_name = settings.exchanges[0]
        exch = ExchangeClient(exchange_name)

        print(f"📡 Polling started (exchange={exchange_name})")

        try:
            while self.running:
                for pair in pairs:
                    try:
                        ticker = await exch.fetch_ticker(pair)

                        payload = {
                            "pair": pair,
                            "ticker": ticker
                        }

                        # Cache for REST fallback
                        await set_cached(
                            f"ticker:{exchange_name}:{pair}",
                            json.dumps(payload),
                            ttl=settings.default_cache_ttl
                        )

                        # Broadcast to clients
                        dead_clients = []

                        for ws in self.clients:
                            try:
                                await ws.send_json(payload)
                            except Exception:
                                dead_clients.append(ws)

                        # Remove dead connections
                        for ws in dead_clients:
                            await self.unregister(ws)

                    except Exception as e:
                        print(f"⚠ Error fetching {pair}:", e)

                await asyncio.sleep(settings.poll_interval)

        except asyncio.CancelledError:
            print("⛔ Poll loop cancelled")

        finally:
            await exch.close()
            print("📡 Polling stopped")
