

from fastapi import FastAPI
from .routes import router
from .broadcaster import Broadcaster

broadcaster = Broadcaster()

app = FastAPI(title="MCP Server")

# 🔥 inject immediately (pytest will see it)
router.broadcaster = broadcaster


@app.on_event("startup")
async def startup_event():
    await broadcaster.start()


@app.on_event("shutdown")
async def shutdown_event():
    await broadcaster.stop()


app.include_router(router, prefix="/api")
