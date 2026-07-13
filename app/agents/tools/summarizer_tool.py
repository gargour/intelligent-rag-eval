from app.vectorstore.retriever import retrieve_relevant_chunks
from app.llm.factory import get_llm_client
from app.llm.prompt_templates.summarize_prompt import SUMMARIZE_SYSTEM_PROMPT, build_summarize_prompt

def summarize_document_tool(document_id: str, top_k: int = 20):
    results = retrieve_relevant_chunks("résumé général du document", document_ids=[document_id], top_k=top_k)
    chunks = [r[0] for r in results]

    if not chunks:
        return "Document introuvable ou vide."

    prompt = build_summarize_prompt(chunks)
    llm = get_llm_client()
    return llm.generate(SUMMARIZE_SYSTEM_PROMPT, prompt)