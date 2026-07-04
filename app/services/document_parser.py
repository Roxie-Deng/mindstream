from pathlib import Path
from pypdf import PdfReader
from pydantic import BaseModel


class Document(BaseModel):
    content: str
    metadata: dict


def parse_document(file_path: str) -> Document:
    path = Path(file_path)

    suffix = path.suffix.lower()
    if suffix == ".md":
        content = _parse_markdown(path)
    elif suffix == ".txt":
        content = _parse_txt(path)
    elif suffix == ".pdf":
        content = _parse_pdf(path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    return Document(
        content=content,
        metadata={
            "file_name": path.name,
            "file_type": suffix,
        },
    )


def _parse_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_pdf(path: Path) -> str:
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        texts.append(page.extract_text())
    return "\n".join(texts)
