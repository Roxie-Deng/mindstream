from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MindStream"
    debug: bool = True

    # LLM settings
    llm_provider: str = "openai"
    llm_api_key: str | None = None
    llm_model: str = "gpt-4o-mini"
    llm_base_url: str | None = None


settings = Settings()