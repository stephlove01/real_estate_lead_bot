"""Health check endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
def health():
    return {
        "status": "ok",
        "service": "real-estate-lead-bot",
        "version": "0.1.0",
    }
