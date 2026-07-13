import hashlib
import json
from pathlib import Path

CACHE_DIR = Path("./data/embedding_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def get_cached_embedding(text: str):
    cache_file = CACHE_DIR / f"{_hash_text(text)}.json"
    if cache_file.exists():
        return json.loads(cache_file.read_text())
    return None

def set_cached_embedding(text: str, embedding: list[float]):
    cache_file = CACHE_DIR / f"{_hash_text(text)}.json"
    cache_file.write_text(json.dumps(embedding))