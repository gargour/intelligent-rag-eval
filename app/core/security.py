from fastapi import Header, HTTPException
from app.config import get_settings

settings = get_settings()

def get_api_key(x_api_key: str = Header(default=None)) -> str:
    if x_api_key != settings.api_secret_key:
        raise HTTPException(status_code=403, detail="Accès refusé")
    return x_api_key