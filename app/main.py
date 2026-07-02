from fastapi import FastAPI
from app.api.router import api_router
from app.config import settings

app = FastAPI(
    title="MindStream",
    description="Personal Knowledge Assistant",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy"}