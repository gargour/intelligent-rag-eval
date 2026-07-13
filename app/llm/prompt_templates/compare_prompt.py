COMPARE_SYSTEM_PROMPT = """Tu es un analyste qui compare des documents de manière factuelle et structurée.
Présente les similitudes et différences sous forme de points clairs, en citant les sources."""

def build_compare_prompt(chunks_doc_a: list, chunks_doc_b: list, question: str) -> str:
    context_a = "\n".join(c.page_content for c in chunks_doc_a)
    context_b = "\n".join(c.page_content for c in chunks_doc_b)
    return f"""DOCUMENT A:
{context_a}

DOCUMENT B:
{context_b}

TÂCHE: {question}

Compare les deux documents ci-dessus de façon structurée (similitudes / différences)."""