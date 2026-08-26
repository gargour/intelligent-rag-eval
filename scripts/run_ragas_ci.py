"""Ingère un document de test fixe et lance une évaluation RAGAS complète (usage CI/planifié)."""
import sys
import json
from pathlib import Path
from datetime import datetime

from app.db.session import SessionLocal, init_db
from app.db.models import Document, Chunk
from app.ingestion.pipeline import ingest_document
from app.evaluation.dataset_builder import generate_qa_pairs
from app.evaluation.ragas_eval import evaluate_rag_dataset
from app.vectorstore.retriever import retrieve_relevant_chunks
from app.rag.chain import run_rag_query

FIXTURE_PATH = Path("tests/fixtures/sample_document.txt")


def main():
    init_db()
    db = SessionLocal()

    existing = db.query(Document).filter(Document.filename == FIXTURE_PATH.name).all()
    for doc in existing:
        db.query(Chunk).filter(Chunk.document_id == doc.id).delete()
        db.delete(doc)
    db.commit()

    doc_id = ingest_document(str(FIXTURE_PATH), FIXTURE_PATH.name, "txt")
    print(f"Document de test ingéré : {doc_id}")

    chunks = db.query(Chunk).filter(Chunk.document_id == doc_id).limit(5).all()

    questions, answers, contexts, ground_truths = [], [], [], []
    for chunk in chunks:
        qa_pairs = generate_qa_pairs(chunk.content, n=1)
        for pair in qa_pairs:
            question = pair.get("question")
            ground_truth = pair.get("answer")
            if not question or not ground_truth:
                continue

            retrieved = retrieve_relevant_chunks(question, document_ids=[doc_id], top_k=5)
            context_list = [d.page_content for d, _ in retrieved]
            rag_result = run_rag_query(question, document_ids=[doc_id])

            questions.append(question)
            answers.append(rag_result.answer)
            contexts.append(context_list if context_list else [""])
            ground_truths.append(ground_truth)

    if not questions:
        print("Aucune question générée, arrêt.")
        sys.exit(1)

    df = evaluate_rag_dataset(questions, answers, contexts, ground_truths)

    result = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_questions": len(df),
        "avg_faithfulness": round(float(df["faithfulness"].mean()), 3),
        "avg_answer_relevancy": round(float(df["answer_relevancy"].mean()), 3),
        "avg_context_precision": round(float(df["context_precision"].mean()), 3),
        "avg_context_recall": round(float(df["context_recall"].mean()), 3),
    }

    print(json.dumps(result, indent=2))
    Path("ragas_report.json").write_text(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()