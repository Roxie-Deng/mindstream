from typing import List
from langchain_core.documents import Document as LCDocument
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.services.embedding_service import EmbeddingService


class VectorStore:
    def __init__(self, embedding_service: EmbeddingService, collection_name: str = "mindstream"):
        self.embedding_service = embedding_service
        self.collection_name = collection_name
        self.client = QdrantClient(":memory:")
        self._vectorstore: QdrantVectorStore | None = None

    def create_collection(self, vector_size: int = 768):
        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )
        self._vectorstore = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedding_service.embedder,
        )

    def upsert_documents(self, documents: List[LCDocument]):
        if self._vectorstore is None:
            self.create_collection()

        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        self._vectorstore.add_texts(texts=texts, metadatas=metadatas)

    def similarity_search(self, query: str, k: int = 4) -> List[LCDocument]:
        if self._vectorstore is None:
            return []
        return self._vectorstore.similarity_search(query=query, k=k)
