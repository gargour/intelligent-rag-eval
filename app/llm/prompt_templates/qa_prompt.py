QA_SYSTEM_PROMPT = """Tu es un assistant de recherche documentaire rigoureux.
Réponds UNIQUEMENT à partir du contexte fourni ci-dessous.
Si l'information n'est pas dans le contexte, dis clairement que tu ne trouves pas la réponse.
Ne jamais inventer d'information."""

def build_qa_prompt(question: str, context_chunks: list) -> str:
    context_text = "\n\n".join(
        f"[Source {i+1} - {c.metadata.get('filename')}, page {c.metadata.get('page', '?')}]\n{c.page_content}"
        for i, c in enumerate(context_chunks)
    )
    return f"""CONTEXTE:
{context_text}

QUESTION:
{question}

Réponds de manière précise et concise en te basant uniquement sur le contexte ci-dessus."""