from __future__ import annotations

import os
from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openbb_core.api.rest_api import app as openbb_app

SERVICE_NAME: Final = "OpenBB MarketDesk API"
DEFAULT_ORIGINS: Final = (
    "http://localhost:3000,"
    "https://openbb-marketdesk-lab.stomper-bdg.chatgpt.site"
)


def parse_origins(value: str) -> list[str]:
    """Return a clean, de-duplicated CORS origin allowlist."""
    origins: list[str] = []
    for item in value.split(","):
        origin = item.strip().rstrip("/")
        if origin and origin not in origins:
            origins.append(origin)
    return origins


allowed_origins = parse_origins(os.getenv("CORS_ORIGINS", DEFAULT_ORIGINS))

# The outer app provides production CORS and health endpoints while preserving
# OpenBB's own FastAPI lifespan and complete /api/v1 route tree.
app = FastAPI(
    title=SERVICE_NAME,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=openbb_app.router.lifespan_context,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Accept", "Authorization", "Content-Type"],
    max_age=3600,
)


@app.get("/health", include_in_schema=False)
async def health() -> dict[str, object]:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "provider": "yfinance",
        "auth_enabled": os.getenv("OPENBB_API_AUTH", "False").lower() == "true",
    }


@app.get("/", include_in_schema=False)
async def service_info() -> dict[str, str]:
    return {
        "service": SERVICE_NAME,
        "status": "ready",
        "health": "/health",
        "docs": "/docs",
        "historical_prices": "/api/v1/equity/price/historical",
    }


app.mount("/", openbb_app)
