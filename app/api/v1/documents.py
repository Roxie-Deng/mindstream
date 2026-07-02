from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

router = APIRouter()

SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


class SyncRequest(BaseModel):
    directory: str


class SyncResponse(BaseModel):
    files: list[str]


@router.post("/sync", response_model=SyncResponse)
def sync_documents(request: SyncRequest):
    dir_path = Path(request.directory)

    if not dir_path.exists():
        raise HTTPException(status_code=404, detail=f"Directory not found: {request.directory}")

    if not dir_path.is_dir():
        raise HTTPException(status_code=400, detail=f"Not a directory: {request.directory}")

    files = [
        str(f.relative_to(dir_path))
        for f in dir_path.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    return SyncResponse(files=files)
