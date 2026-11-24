from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Nexus RAG Engine"
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    chroma_persist_dir: str = "./chroma_data"
    chunk_size: int = 800
    chunk_overlap: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
