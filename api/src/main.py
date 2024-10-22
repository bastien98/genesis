from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.v2 import router as v2
from config import APP_NAME, APP_VERSION

load_dotenv()

app = FastAPI(title=APP_NAME)
app.include_router(v2)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def check_health() -> dict[str, str]:
    """Liveness check for the chat-api."""

    return {"version": APP_VERSION}


@app.get("/ready")
async def check_readiness() -> str:
    """Readiness check for the chat-api."""

    return "Ready"
