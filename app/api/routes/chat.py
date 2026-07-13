from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import ChatLog
from app.api.schemas.chat_schema import QueryRequest, AnswerResponse
from app.agents.agent_router import route_request
from app.rag.chain import run_rag_query
import json

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