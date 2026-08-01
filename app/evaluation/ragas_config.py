from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from app.config import get_settings

settings = get_settings()

def get_ragas_llm():
    """LLM utilisé par RAGAS (via Groq, compatible OpenAI), enveloppé pour RAGAS 0.2+."""
    llm = ChatOpenAI(
        model=settings.grok_model,
        api_key=settings.grok_api_key,
        base_url=settings.grok_base_url,
        temperature=0,
    )
    return LangchainLLMWrapper(llm)

def get_ragas_embeddings():
    """Embeddings utilisés par RAGAS, enveloppés pour RAGAS 0.2+."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return LangchainEmbeddingsWrapper(embeddings)