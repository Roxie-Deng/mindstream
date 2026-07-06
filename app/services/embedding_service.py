from typing import List
from langchain_core.embeddings import Embeddings
from pydantic import BaseModel
import os


class MockEmbeddings(Embeddings):
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [[0.1] * 768 for _ in texts]

    def embed_query(self, query: str) -> List[float]:
        return [0.1] * 768


class EmbeddingConfig(BaseModel):
    model: str = "models/text-embedding-004"
    google_api_key: str | None = None


class EmbeddingService:
    def __init__(self, config: EmbeddingConfig):
        self.config = config
        if config.google_api_key:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            self.embedder = GoogleGenerativeAIEmbeddings(
                model=config.model,
                google_api_key=config.google_api_key,
            )
        else:
            self.embedder = MockEmbeddings()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embedder.embed_documents(texts)

    def embed_query(self, query: str) -> List[float]:
        return self.embedder.embed_query(query)
