from fastapi import Header, HTTPException
from app.config import get_settings

settings = get_settings()

def verify_api_key(x_api_key: str = Header(default=None)):
    """Dépendance optionnelle de sécurité pour protéger les routes sensibles."""
    if settings.api_secret_key and settings.api_secret_key != "change-me":
        if x_api_key != settings.api_secret_key:
            raise HTTPException(status_code=401, detail="Clé API invalide")
    return True