from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from file_api.api.v1 import router as v1
from file_api.config import APP_VERSION, APP_NAME

app = FastAPI(title=APP_NAME)
app.include_router(v1)

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