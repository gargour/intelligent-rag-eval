from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Document, Chunk, EvalResult
from app.api.schemas.eval_schema import EvalRunRequest, EvalRunResponse, EvalMetricResult
from app.evaluation.dataset_builder import generate_qa_pairs
from app.evaluation.llm_judge import judge_answer
from app.evaluation.metrics import context_precision_score, context_recall_score
from app.rag.chain import run_rag_query
import uuid

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

@router.post("/run", response_model=EvalRunResponse)
def run_evaluation(request: EvalRunRequest, db: Session = Depends(get_db)):
    query = db.query(Chunk)
    if request.document_ids:
        query = query.filter(Chunk.document_id.in_(request.document_ids))
    chunks = query.limit(20).all()  # échantillon pour limiter le coût API

    details = []
    for chunk in chunks:
        qa_pairs = generate_qa_pairs(chunk.content, n=request.num_questions_per_doc)

        for pair in qa_pairs:
            question = pair.get("question")
            ground_truth = pair.get("answer")
            if not question:
                continue

            rag_result = run_rag_query(question, document_ids=[chunk.document_id])
            context_text = "\n".join(c.snippet for c in rag_result.citations)

            judgment = judge_answer(question, rag_result.answer, ground_truth, context_text)

            eval_record = EvalResult(
                id=str(uuid.uuid4()),
                question=question,
                generated_answer=rag_result.answer,
                ground_truth=ground_truth,
                faithfulness=judgment.get("faithfulness", 0.0),
                answer_relevance=judgment.get("relevance", 0.0),
                context_precision=context_precision_score(context_text, ground_truth),
                context_recall=context_recall_score(rag_result.answer, ground_truth),
            )
            db.add(eval_record)

            details.append(EvalMetricResult(
                question=question,
                generated_answer=rag_result.answer,
                ground_truth=ground_truth,
                faithfulness=judgment.get("faithfulness", 0.0),
                answer_relevance=judgment.get("relevance", 0.0),
                context_precision=context_precision_score(context_text, ground_truth),
                context_recall=context_recall_score(rag_result.answer, ground_truth),
            ))
            
    db.commit()

    if not details:
        return EvalRunResponse(
            total_questions=0, avg_faithfulness=0, avg_answer_relevance=0,
            avg_context_precision=0, avg_context_recall=0, details=[]
        )

    avg_f = sum(d.faithfulness for d in details) / len(details)
    avg_r = sum(d.answer_relevance for d in details) / len(details)

    return EvalRunResponse(
        total_questions=len(details),
        avg_faithfulness=round(avg_f, 3),
        avg_answer_relevance=round(avg_r, 3),
        avg_context_precision=0.0,
        avg_context_recall=0.0,
        details=details,
    )