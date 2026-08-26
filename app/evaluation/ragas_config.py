from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from app.config import get_settings

settings = get_settings()

def get_ragas_llm():
    """LLM utilisé par RAGAS — clé Groq dédiée."""
    # Correction ici pour utiliser la clé dédiée RAGAS
    ragas_key = settings.grok_api_key_ragas or settings.grok_api_key
    
    llm = ChatOpenAI(
        model=settings.grok_model,
        api_key=ragas_key,
        base_url=settings.grok_base_url,
        temperature=0,
        request_timeout=60,
    )
    return LangchainLLMWrapper(llm)

def get_ragas_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return LangchainEmbeddingsWrapper(embeddings)