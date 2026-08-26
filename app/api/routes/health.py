from fastapi import APIRouter
from app.llm.factory import get_llm_client

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/health/groq")
def groq_health_check():
    """Vérifie si l'API Groq (clé principale) répond sans erreur de quota."""
    try:
        llm = get_llm_client()
        llm.generate("Tu es un assistant.", "Dis juste 'ok'.")
        return {"status": "ok", "message": "Groq disponible"}
    except Exception as e:
        error_str = str(e)
        if "rate_limit" in error_str or "429" in error_str:
            return {"status": "quota_exceeded", "message": "Quota Groq épuisé"}
        return {"status": "error", "message": error_str[:200]}