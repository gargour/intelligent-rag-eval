import json
import re
from app.llm.grok_client import GrokClient
from app.config import get_settings

settings = get_settings()

JUDGE_SYSTEM_PROMPT = """Tu es un évaluateur strict mais juste de systèmes RAG.
Compare la réponse générée à la réponse de référence, en te basant sur le sens, pas la formulation exacte.
Si la réponse générée contient la même information factuelle que la référence (même avec des mots différents), considère-la comme correcte.

Réponds STRICTEMENT en JSON valide, sans aucun texte avant ou après, sous cette forme exacte:
{"faithfulness": 0.0, "relevance": 0.0, "justification": "..."}

Règles de notation:
- faithfulness = 1.0 si la réponse est fidèle au contexte fourni (pas d'invention), 0.0 si elle contredit ou invente
- relevance = 1.0 si la réponse répond correctement à la question par rapport à la référence, 0.0 si incorrecte ou hors sujet
- Utilise des valeurs intermédiaires (0.5, 0.7...) si partiellement correct"""

def _extract_json(raw: str) -> dict:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(json)?", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    return {"faithfulness": None, "relevance": None, "justification": "Erreur de parsing JSON"}


def judge_answer(question: str, generated_answer: str, ground_truth: str, context: str) -> dict:
    api_key = settings.grok_api_key_judge or settings.grok_api_key
    llm = GrokClient(api_key=api_key)

    prompt = f"""QUESTION: {question}

CONTEXTE UTILISÉ PAR LE RAG:
{context}

RÉPONSE GÉNÉRÉE:
{generated_answer}

RÉPONSE DE RÉFÉRENCE (ground truth):
{ground_truth}

Évalue la faithfulness et la relevance selon les règles données."""

    raw = llm.generate(JUDGE_SYSTEM_PROMPT, prompt)
    result = _extract_json(raw)

    if result.get("faithfulness") is None or result.get("relevance") is None:
        raw_retry = llm.generate(
            JUDGE_SYSTEM_PROMPT + "\n\nIMPORTANT: réponds UNIQUEMENT avec le JSON, rien d'autre.",
            prompt,
        )
        result = _extract_json(raw_retry)

    return {
        "faithfulness": result.get("faithfulness") or 0.0,
        "relevance": result.get("relevance") or 0.0,
        "justification": result.get("justification", ""),
    }