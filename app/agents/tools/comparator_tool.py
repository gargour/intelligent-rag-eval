from app.vectorstore.retriever import retrieve_relevant_chunks
from app.llm.factory import get_llm_client
from app.llm.prompt_templates.compare_prompt import COMPARE_SYSTEM_PROMPT, build_compare_prompt

def compare_documents_tool(document_id_a: str, document_id_b: str, question: str, top_k: int = 10):
    results_a = retrieve_relevant_chunks(question, document_ids=[document_id_a], top_k=top_k)
    results_b = retrieve_relevant_chunks(question, document_ids=[document_id_b], top_k=top_k)

    chunks_a = [r[0] for r in results_a]
    chunks_b = [r[0] for r in results_b]

    prompt = build_compare_prompt(chunks_a, chunks_b, question)
    llm = get_llm_client()
    return llm.generate(COMPARE_SYSTEM_PROMPT, prompt)