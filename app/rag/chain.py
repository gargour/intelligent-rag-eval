import time
from app.vectorstore.retriever import retrieve_relevant_chunks
from app.rag.reranker import rerank
from app.llm.factory import get_llm_client
from app.llm.prompt_templates.qa_prompt import QA_SYSTEM_PROMPT, build_qa_prompt
from app.rag.citation_builder import build_citations
from app.api.schemas.chat_schema import AnswerResponse

def run_rag_query(question: str, document_ids: list = None, top_k: int = 5, use_reranker: bool = True) -> AnswerResponse:
    start = time.time()

    # Récupère plus de candidats que nécessaire pour laisser le reranker affiner
    fetch_k = top_k * 4 if use_reranker else top_k
    results = retrieve_relevant_chunks(question, document_ids=document_ids, top_k=fetch_k)

    if not results:
        return AnswerResponse(
            answer="Aucune information pertinente trouvée dans les documents fournis.",
            citations=[],
            latency_ms=int((time.time() - start) * 1000),
        )

    if use_reranker and len(results) > top_k:
        reranked = rerank(question, results, top_k=top_k)
        # rerank retourne (Document, cross_encoder_score); on garde le score FAISS d'origine pour les citations
        original_scores = {id(doc): score for doc, score in results}
        results = [(doc, original_scores.get(id(doc), score)) for doc, score in reranked]
    else:
        results = results[:top_k]

    chunks = [r[0] for r in results]
    prompt = build_qa_prompt(question, chunks)

    llm = get_llm_client()
    answer = llm.generate(QA_SYSTEM_PROMPT, prompt)

    citations = build_citations(results)
    latency = int((time.time() - start) * 1000)

    return AnswerResponse(answer=answer, citations=citations, latency_ms=latency)