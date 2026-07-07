from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
import os


class LLMConfig(BaseModel):
    provider: str = "openai"
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini"
    base_url: Optional[str] = None


class LLMProvider(ABC):
    @abstractmethod
    def get_model(self) -> BaseChatModel:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self, config: LLMConfig):
        self.config = config

    def get_model(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.config.model,
            api_key=self.config.api_key,
            base_url=self.config.base_url,
        )


class MinimaxProvider(LLMProvider):
    def __init__(self, config: LLMConfig):
        self.config = config

    def get_model(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.config.model,
            api_key=self.config.api_key,
            base_url=self.config.base_url or "https://api.minimax.chat/v1",
        )


class GeminiProvider(LLMProvider):
    def __init__(self, config: LLMConfig):
        self.config = config

    def get_model(self) -> BaseChatModel:
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=self.config.model,
            google_api_key=self.config.api_key,
        )


class OllamaProvider(LLMProvider):
    def __init__(self, config: LLMConfig):
        self.config = config

    def get_model(self) -> BaseChatModel:
        return ChatOpenAI(
            model=self.config.model,
            api_key="ollama",
            base_url=self.config.base_url or "http://localhost:11434/v1",
        )


class LLMService:
    def __init__(self, config: LLMConfig):
        self.config = config
        self._provider = self._create_provider()

    def _create_provider(self) -> LLMProvider:
        providers = {
            "openai": OpenAIProvider,
            "minimax": MinimaxProvider,
            "gemini": GeminiProvider,
            "ollama": OllamaProvider,
        }
        provider_class = providers.get(self.config.provider)
        if not provider_class:
            raise ValueError(f"Unknown provider: {self.config.provider}")
        return provider_class(self.config)

    def generate(self, question: str, context: str) -> str:
        model = self._provider.get_model()
        prompt = f"""Based on the following context, answer the question.

Context:
{context}

Question: {question}

Answer:"""
        response = model.invoke(prompt)
        return response.content
