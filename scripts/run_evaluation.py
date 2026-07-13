"""Lance une évaluation complète et sauvegarde un rapport JSON."""
import json
from datetime import datetime
from pathlib import Path
from app.db.session import SessionLocal
from app.db.models import Chunk
from app.evaluation.dataset_builder import generate_qa_pairs
from app.evaluation.llm_judge import judge_answer
from app.rag.chain import run_rag_query

REPORT_DIR = Path("./app/evaluation/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    db = SessionLocal()
    chunks = db.query(Chunk).limit(15).all()

    results = []
    for chunk in chunks:
        qa_pairs = generate_qa_pairs(chunk.content, n=2)
        for pair in qa_pairs:
            question = pair.get("question")
            ground_truth = pair.get("answer")
            if not question:
                continue

            rag_result = run_rag_query(question, document_ids=[chunk.document_id])
            context_text = "\n".join(c.snippet for c in rag_result.citations)
            judgment = judge_answer(question, rag_result.answer, ground_truth, context_text)

            results.append({
                "question": question,
                "generated_answer": rag_result.answer,
                "ground_truth": ground_truth,
                "faithfulness": judgment.get("faithfulness", 0.0),
                "relevance": judgment.get("relevance", 0.0),
            })

    report = {
        "timestamp": datetime.utcnow().isoformat(),
        "total_questions": len(results),
        "avg_faithfulness": sum(r["faithfulness"] for r in results) / len(results) if results else 0,
        "avg_relevance": sum(r["relevance"] for r in results) / len(results) if results else 0,
        "details": results,
    }

    report_file = REPORT_DIR / f"eval_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"Rapport sauvegardé: {report_file}")
    db.close()

if __name__ == "__main__":
    main()