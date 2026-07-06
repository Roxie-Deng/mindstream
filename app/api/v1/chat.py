from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.vector_store import VectorStore
from app.api.v1.documents import get_vector_store

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[dict]


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    vs: VectorStore = get_vector_store()

    docs = vs.similarity_search(request.question, k=4)

    if not docs:
        raise HTTPException(status_code=404, detail="No relevant documents found")

    context = "\n\n".join([doc.page_content for doc in docs])
    answer = f"Based on {len(docs)} relevant documents: {context[:200]}..."

    return ChatResponse(
        answer=answer,
        sources=[
            {
                "content": doc.page_content[:100],
                "metadata": doc.metadata,
            }
            for doc in docs
        ],
    )
