import time
from app.vectorstore.retriever import retrieve_relevant_chunks
from app.llm.factory import get_llm_client
from app.llm.prompt_templates.compare_prompt import COMPARE_SYSTEM_PROMPT, build_compare_prompt
from app.core.logging import logger

def compare_documents_tool(document_id_a: str, document_id_b: str, question: str, top_k: int = 10):
    t0 = time.time()

    results_a = retrieve_relevant_chunks(question, document_ids=[document_id_a], top_k=top_k)
    t1 = time.time()
    logger.info(f"[TIMING] Recherche doc A : {t1 - t0:.2f}s")

    results_b = retrieve_relevant_chunks(question, document_ids=[document_id_b], top_k=top_k)
    t2 = time.time()
    logger.info(f"[TIMING] Recherche doc B : {t2 - t1:.2f}s")

    chunks_a = [r[0] for r in results_a]
    chunks_b = [r[0] for r in results_b]

    prompt = build_compare_prompt(chunks_a, chunks_b, question)
    t3 = time.time()
    logger.info(f"[TIMING] Construction prompt : {t3 - t2:.2f}s")

    llm = get_llm_client()
    result = llm.generate(COMPARE_SYSTEM_PROMPT, prompt)
    t4 = time.time()
    logger.info(f"[TIMING] Appel LLM (Groq) : {t4 - t3:.2f}s")
    logger.info(f"[TIMING] TOTAL : {t4 - t0:.2f}s")

    return result