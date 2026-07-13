from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import get_settings

settings = get_settings()
_embedder_instance = None

def get_embedder():
    global _embedder_instance
    if _embedder_instance is not None:
        return _embedder_instance

    if settings.embedding_provider == "openai":
        _embedder_instance = OpenAIEmbeddings(
            model=settings.embedding_model,
            api_key=settings.openai_api_key,
        )
    elif settings.embedding_provider == "sentence-transformers":
        _embedder_instance = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
    else:
        raise ValueError(f"Provider d'embedding inconnu: {settings.embedding_provider}")

    return _embedder_instance