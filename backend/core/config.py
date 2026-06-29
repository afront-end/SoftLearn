from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str
    redis_url: str = "redis://localhost:6379"
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5-coder"
    ollama_embedding_model: str = "nomic-embed-text"
    secret_key: str
    access_token_expire_minutes: int = 10080
    algorithm: str = "HS256"

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str 
    smtp_password: str 
    smtp_from: str

    google_client_id: str 


settings = Settings()
