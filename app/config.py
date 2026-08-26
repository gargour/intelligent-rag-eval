from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # LLM - Grok / Groq
    grok_api_key: str = ""
    grok_api_key_ragas: str = ""
    grok_api_key_judge: str = ""
    groq_api_key_ragas: str = ""
    groq_api_key_judge: str = ""
    grok_model: str = "openai/gpt-oss-20b"
    grok_base_url: str = "https://api.x.ai/v1"
    llm_provider: str = "grok"

    # Embeddings
    openai_api_key: str = ""
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"

    # Vectorstore - FAISS
    vectorstore_provider: str = "faiss"
    faiss_index_dir: str = "./data/faiss_index"

    # DB
    database_url: str = "postgresql://raguser:ragpass@localhost:5432/ragdb"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_secret_key: str = "change-me"
    api_base_url: str = "http://localhost:8000"

    # RAG params
    chunk_size: int = 1000
    chunk_overlap: int = 150
    top_k_retrieval: int = 5

    model_config = {"env_file": ".env", "extra": "ignore"}

@lru_cache
def get_settings() -> Settings:
    return Settings()