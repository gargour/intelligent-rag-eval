from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Chunk, EvalResult
from app.api.schemas.eval_schema import EvalRunRequest, EvalRunResponse, EvalMetricResult
from app.evaluation.dataset_builder import generate_qa_pairs
from app.evaluation.llm_judge import judge_answer
from app.evaluation.metrics import context_precision_score, context_recall_score
from app.rag.chain import run_rag_query
from app.core.logging import logger
import uuid
import traceback
from app.evaluation.ragas_eval import evaluate_rag_dataset
from app.api.schemas.eval_schema import RagasEvalResponse, RagasResultRow
from app.vectorstore.retriever import retrieve_relevant_chunks
import json as jsonlib
from datetime import datetime
from pathlib import Path

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.post("/run", response_model=EvalRunResponse)
def run_evaluation(request: EvalRunRequest, db: Session = Depends(get_db)):
    query = db.query(Chunk)
    if request.document_ids:
        query = query.filter(Chunk.document_id.in_(request.document_ids))
    chunks = query.limit(20).all()

    if not chunks:
        raise HTTPException(status_code=404, detail="Aucun chunk trouvé pour les documents sélectionnés.")

    details = []
    errors_count = 0

    for chunk in chunks:
        try:
            qa_pairs = generate_qa_pairs(chunk.content, n=request.num_questions_per_doc)
        except Exception as e:
            logger.error(f"Erreur génération QA pour chunk {chunk.id}: {e}\n{traceback.format_exc()}")
            errors_count += 1
            continue

        for pair in qa_pairs:
            question = pair.get("question")
            ground_truth = pair.get("answer")
            if not question or not ground_truth:
                continue

            try:
                rag_result = run_rag_query(question, document_ids=[chunk.document_id])
                context_text = "\n".join(c.snippet for c in rag_result.citations)

                judgment = judge_answer(question, rag_result.answer, ground_truth, context_text)
                precision = context_precision_score(context_text, ground_truth)
                recall = context_recall_score(rag_result.answer, ground_truth)

                eval_record = EvalResult(
                    id=str(uuid.uuid4()),
                    question=question,
                    generated_answer=rag_result.answer,
                    ground_truth=ground_truth,
                    faithfulness=judgment.get("faithfulness", 0.0),
                    answer_relevance=judgment.get("relevance", 0.0),
                    context_precision=precision,
                    context_recall=recall,
                )
                db.add(eval_record)

                details.append(EvalMetricResult(
                    question=question,
                    generated_answer=rag_result.answer,
                    ground_truth=ground_truth,
                    faithfulness=judgment.get("faithfulness", 0.0),
                    answer_relevance=judgment.get("relevance", 0.0),
                    context_precision=precision,
                    context_recall=recall,
                ))

            except Exception as e:
                logger.error(f"Erreur évaluation question '{question}': {e}\n{traceback.format_exc()}")
                errors_count += 1
                continue

    db.commit()

    if not details:
        raise HTTPException(
            status_code=500,
            detail=f"Aucune évaluation n'a pu être complétée ({errors_count} erreurs). Vérifiez les logs serveur.",
        )

    avg_f = sum(d.faithfulness for d in details) / len(details)
    avg_r = sum(d.answer_relevance for d in details) / len(details)
    avg_p = sum(d.context_precision for d in details) / len(details)
    avg_rec = sum(d.context_recall for d in details) / len(details)

    return EvalRunResponse(
        total_questions=len(details),
        avg_faithfulness=round(avg_f, 3),
        avg_answer_relevance=round(avg_r, 3),
        avg_context_precision=round(avg_p, 3),
        avg_context_recall=round(avg_rec, 3),
        details=details,
    )

@router.post("/ragas", response_model=RagasEvalResponse)
def run_ragas_evaluation(request: EvalRunRequest, db: Session = Depends(get_db)):
    query = db.query(Chunk)
    if request.document_ids:
        query = query.filter(Chunk.document_id.in_(request.document_ids))
    chunks = query.limit(10).all()  # échantillon limité, RAGAS fait beaucoup d'appels LLM

    if not chunks:
        raise HTTPException(status_code=404, detail="Aucun chunk trouvé pour les documents sélectionnés.")

    questions, answers, contexts, ground_truths = [], [], [], []

    for chunk in chunks:
        try:
            qa_pairs = generate_qa_pairs(chunk.content, n=request.num_questions_per_doc)
        except Exception as e:
            logger.error(f"Erreur génération QA pour chunk {chunk.id}: {e}")
            continue

        for pair in qa_pairs:
            question = pair.get("question")
            ground_truth = pair.get("answer")
            if not question or not ground_truth:
                continue

            try:
                retrieved = retrieve_relevant_chunks(question, document_ids=[chunk.document_id], top_k=5)
                context_list = [doc.page_content for doc, _ in retrieved]

                rag_result = run_rag_query(question, document_ids=[chunk.document_id])

                questions.append(question)
                answers.append(rag_result.answer)
                contexts.append(context_list if context_list else [""])
                ground_truths.append(ground_truth)
            except Exception as e:
                logger.error(f"Erreur RAG pour question '{question}': {e}")
                continue

    if not questions:
        raise HTTPException(status_code=500, detail="Aucune donnée valide pour l'évaluation RAGAS.")

    df = evaluate_rag_dataset(questions, answers, contexts, ground_truths)

    details = [
        RagasResultRow(
            question=row["user_input"],
            answer=row["response"],
            ground_truth=row.get("reference"),
            faithfulness=round(float(row["faithfulness"]), 3) if row["faithfulness"] == row["faithfulness"] else 0.0,
            answer_relevancy=round(float(row["answer_relevancy"]), 3) if row["answer_relevancy"] == row["answer_relevancy"] else 0.0,
            context_precision=round(float(row["context_precision"]), 3) if row["context_precision"] == row["context_precision"] else 0.0,
            context_recall=round(float(row["context_recall"]), 3) if row["context_recall"] == row["context_recall"] else 0.0,
        )
        for _, row in df.iterrows()
    ]

    return RagasEvalResponse(
        total_questions=len(details),
        avg_faithfulness=round(df["faithfulness"].mean(), 3),
        avg_answer_relevancy=round(df["answer_relevancy"].mean(), 3),
        avg_context_precision=round(df["context_precision"].mean(), 3),
        avg_context_recall=round(df["context_recall"].mean(), 3),
        details=details,
    )
