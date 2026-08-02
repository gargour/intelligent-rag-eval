import json
import re
from app.llm.factory import get_llm_client
from app.llm.prompt_templates.agent_router_prompt import AGENT_ROUTER_SYSTEM_PROMPT, build_router_prompt
from app.agents.tools.search_tool import search_documents_tool
from app.agents.tools.summarizer_tool import summarize_document_tool
from app.agents.tools.comparator_tool import compare_documents_tool
from app.agents.tools.report_generator_tool import generate_report_tool


def _extract_json(raw: str) -> dict:
    cleaned = raw.strip().strip("```json").strip("```").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    return {"action": "qa", "target_document_ids": [], "reasoning": "fallback: parsing échoué"}


def classify_intent(question: str, available_documents: list) -> dict:
    llm = get_llm_client()
    prompt = build_router_prompt(question, available_documents)
    raw = llm.generate(AGENT_ROUTER_SYSTEM_PROMPT, prompt)
    return _extract_json(raw)


def run_smart_agent(question: str, available_documents: list, document_ids: list = None):
    intent = classify_intent(question, available_documents)
    action = intent.get("action", "qa")
    reasoning = intent.get("reasoning", "")

    # Priorité : document_ids fourni explicitement par l'utilisateur > ce que l'agent a détecté > tous les documents
    target_ids = document_ids or intent.get("target_document_ids") or [d["id"] for d in available_documents]

    if action == "summarize":
        if not target_ids:
            result = "Aucun document identifié pour générer un résumé."
        else:
            result = summarize_document_tool(target_ids[0])

    elif action == "compare":
        if len(target_ids) < 2:
            result = "Il faut au moins deux documents identifiés pour effectuer une comparaison."
        else:
            result = compare_documents_tool(target_ids[0], target_ids[1], question)

    elif action == "report":
        result = generate_report_tool(question, document_ids=target_ids)

    else:  # "qa" par défaut
        rag_result = search_documents_tool(question, document_ids=target_ids)
        result = rag_result.answer if hasattr(rag_result, "answer") else rag_result

    return {
        "action": action,
        "reasoning": reasoning,
        "result": result,
    }