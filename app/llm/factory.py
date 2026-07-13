from app.config import get_settings
from app.llm.grok_client import GrokClient

settings = get_settings()

def get_llm_client():
    if settings.llm_provider == "grok":
        return GrokClient()
    raise ValueError(f"Provider LLM inconnu: {settings.llm_provider}")