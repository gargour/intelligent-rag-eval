REPORT_SYSTEM_PROMPT = """Tu es un rédacteur de rapports professionnels.
Génère un rapport structuré (introduction, développement, conclusion) basé strictement sur le contexte fourni."""

def build_report_prompt(chunks: list, topic: str) -> str:
    context_text = "\n\n".join(c.page_content for c in chunks)
    return f"""CONTEXTE:
{context_text}

SUJET DU RAPPORT: {topic}

Rédige un rapport structuré avec titres de sections."""