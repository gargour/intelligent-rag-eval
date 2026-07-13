import json
from app.llm.factory import get_llm_client

GEN_QA_SYSTEM = """Tu génères des paires question/réponse de test à partir d'un texte,
pour évaluer un système de question-réponse documentaire.
Réponds STRICTEMENT en JSON, sous la forme d'une liste d'objets {"question": ..., "answer": ...}.
Aucun texte avant ou après le JSON."""

def generate_qa_pairs(chunk_text: str, n: int = 3) -> list[dict]:
    llm = get_llm_client()
    prompt = f"""Voici un extrait de document:
{chunk_text}

Génère {n} paires question/réponse factuelles à partir de ce texte, au format JSON strict."""

    raw = llm.generate(GEN_QA_SYSTEM, prompt)

    try:
        cleaned = raw.strip().strip("```json").strip("```").strip()
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return []