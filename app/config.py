from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "MindStream"
    debug: bool = True


settings = Settings()