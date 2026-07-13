import time
from app.vectorstore.retriever import retrieve_relevant_chunks
from app.llm.factory import get_llm_client
from app.llm.prompt_templates.qa_prompt import QA_SYSTEM_PROMPT, build_qa_prompt
from app.rag.citation_builder import build_citations
from app.api.schemas.chat_schema import AnswerResponse

def run_rag_query(question: str, document_ids: list = None, top_k: int = 5) -> AnswerResponse:
    start = time.time()

    results = retrieve_relevant_chunks(question, document_ids=document_ids, top_k=top_k)

    if not results:
        return AnswerResponse(
            answer="Aucune information pertinente trouvée dans les documents fournis.",
            citations=[],
            latency_ms=int((time.time() - start) * 1000),
        )

    chunks = [r[0] for r in results]
    prompt = build_qa_prompt(question, chunks)

    llm = get_llm_client()
    answer = llm.generate(QA_SYSTEM_PROMPT, prompt)

    citations = build_citations(results)
    latency = int((time.time() - start) * 1000)

    return AnswerResponse(answer=answer, citations=citations, latency_ms=latency)