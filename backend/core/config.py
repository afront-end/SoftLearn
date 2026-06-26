from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str
    redis_url: str = "redis://localhost:6379"
    gemini_api_key: str = ""
    ollama_url: str = "http://localhost:11434"
    secret_key: str
    access_token_expire_minutes: int = 10080
    algorithm: str = "HS256"


settings = Settings()
