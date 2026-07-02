from fastapi import APIRouter

api_router = APIRouter()

from app.api.v1 import health
api_router.include_router(health.router, prefix="/health", tags=["health"])