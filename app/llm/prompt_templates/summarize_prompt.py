SUMMARIZE_SYSTEM_PROMPT = """Tu es un assistant qui résume des documents de façon claire et structurée,
en conservant les points clés et les chiffres importants."""

def build_summarize_prompt(chunks: list) -> str:
    context_text = "\n\n".join(c.page_content for c in chunks)
    return f"""Voici le contenu du document:
{context_text}

Fais un résumé structuré en 5 à 8 points clés maximum."""