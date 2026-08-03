from fastapi.responses import StreamingResponse
from app.vectorstore.retriever import retrieve_relevant_chunks
from app.rag.reranker import rerank
from app.llm.prompt_templates.qa_prompt import QA_SYSTEM_PROMPT, build_qa_prompt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import ChatLog
from app.api.schemas.chat_schema import QueryRequest, AnswerResponse
from app.agents.agent_router import route_request
from app.rag.chain import run_rag_query
import json
from app.agents.smart_agent import run_smart_agent
from app.api.schemas.chat_schema import SmartAgentRequest, SmartAgentResponse
from app.db.models import Document

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/ask", response_model=AnswerResponse)
def ask_question(request: QueryRequest, db: Session = Depends(get_db)):
    result = run_rag_query(
        question=request.question,
        document_ids=request.document_ids,
        top_k=request.top_k,
    )

    log = ChatLog(
        question=request.question,
        answer=result.answer,
        citations=json.dumps([c.model_dump() for c in result.citations]),
        latency_ms=result.latency_ms,
    )
    db.add(log)
    db.commit()

    return result


@router.post("/agent")
def ask_agent(mode: str, payload: dict, db: Session = Depends(get_db)):
    result = route_request(mode, **payload)
    return {"result": result}

@router.post("/smart", response_model=SmartAgentResponse)
def ask_smart_agent(request: SmartAgentRequest, db: Session = Depends(get_db)):
    all_docs = db.query(Document).filter(Document.status == "ready").all()
    available_documents = [{"id": d.id, "filename": d.filename} for d in all_docs]

    output = run_smart_agent(
        question=request.question,
        available_documents=available_documents,
        document_ids=request.document_ids,
    )

    return SmartAgentResponse(**output)

@router.post("/ask/stream")
def ask_question_stream(request: QueryRequest):
    def generate():
        results = retrieve_relevant_chunks(request.question, document_ids=request.document_ids, top_k=request.top_k * 4)
        if not results:
            yield "Aucune information pertinente trouvée dans les documents fournis."
            return

        if len(results) > request.top_k:
            reranked = rerank(request.question, results, top_k=request.top_k)
            original_scores = {id(doc): score for doc, score in results}
            results = [(doc, original_scores.get(id(doc), score)) for doc, score in reranked]
        else:
            results = results[:request.top_k]

        chunks = [r[0] for r in results]
        prompt = build_qa_prompt(request.question, chunks)

        llm = get_llm_client()
        for token in llm.generate_stream(QA_SYSTEM_PROMPT, prompt):
            yield token

    return StreamingResponse(generate(), media_type="text/plain")