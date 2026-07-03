"""Health check endpoints."""

from fastapi import APIRouter

from app.settings import settings

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
    }


@router.get("/api/v1/health")
async def health_v1() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": "0.1.0",
    }
