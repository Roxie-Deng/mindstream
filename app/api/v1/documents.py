from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import List

from app.services.document_parser import parse_document
from app.services.chunk_service import chunk_documents

router = APIRouter()

SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


class SyncRequest(BaseModel):
    directory: str


class SyncResponse(BaseModel):
    files_found: int
    chunks_created: int


@router.post("/sync", response_model=SyncResponse)
def sync_documents(request: SyncRequest):
    dir_path = Path(request.directory)

    if not dir_path.exists():
        raise HTTPException(status_code=404, detail=f"Directory not found: {request.directory}")

    if not dir_path.is_dir():
        raise HTTPException(status_code=400, detail=f"Not a directory: {request.directory}")

    files = [
        f
        for f in dir_path.rglob("*")
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    all_documents = []
    for f in files:
        docs = parse_document(str(f))
        all_documents.extend(docs)

    chunks = chunk_documents(all_documents)

    return SyncResponse(
        files_found=len(files),
        chunks_created=len(chunks),
    )
