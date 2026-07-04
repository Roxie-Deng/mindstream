from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

from app.services.document_parser import parse_document

router = APIRouter()

SUPPORTED_EXTENSIONS = {".md", ".txt", ".pdf"}


class SyncRequest(BaseModel):
    directory: str


class SyncResponse(BaseModel):
    files: list[str]


class ParseRequest(BaseModel):
    file_path: str


class ParseResponse(BaseModel):
    content: str
    metadata: dict


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


@router.post("/parse", response_model=ParseResponse)
def parse_doc(request: ParseRequest):
    path = Path(request.file_path)

    if not path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {request.file_path}")

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {path.suffix}")

    doc = parse_document(str(path))
    return ParseResponse(content=doc.content, metadata=doc.metadata)
