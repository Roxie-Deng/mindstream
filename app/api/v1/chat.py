from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.vector_store import VectorStore
from app.services.llm_service import LLMService, LLMConfig
from app.config import settings
from app.api.v1.documents import get_vector_store

router = APIRouter()

_llm_service: LLMService | None = None


def get_llm_service() -> LLMService:
    global _llm_service
    if _llm_service is None:
        config = LLMConfig(
            provider=settings.llm_provider,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
            base_url=settings.llm_base_url,
        )
        _llm_service = LLMService(config)
    return _llm_service


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

    llm = get_llm_service()
    answer = llm.generate(request.question, context)

    return ChatResponse(
        answer=answer,
        sources=[
            {
                "content": doc.page_content[:200],
                "metadata": doc.metadata,
            }
            for doc in docs
        ],
    )
