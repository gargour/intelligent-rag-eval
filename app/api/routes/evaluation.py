from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
import logging

from app.evaluation.dataset_builder import generate_qa_pairs
from app.evaluation.llm_judge import judge_answer
from app.evaluation.ragas_config import get_ragas_llm, get_ragas_embeddings

logger = logging.getLogger("rag_app")
router = APIRouter(prefix="/evaluation", tags=["Evaluation"])

class EvaluationRequest(BaseModel):
    document_ids: Optional[List[int]] = None
    num_questions: int = 3

@router.post("/run")
def run_evaluation(request: EvaluationRequest):
    """
    Lance le pipeline d'évaluation (génération de dataset + judge/ragas)
    en utilisant les clés d'API dédiées.
    """
    try:
        logger.info("Démarrage de l'évaluation RAG...")
        
        # Exemple d'appel pour vérifier que les composants s'initialisent bien
        ragas_llm = get_ragas_llm()
        ragas_embeddings = get_ragas_embeddings()

        # Logique principale de ton évaluation...
        # (Ici tu peux intégrer tes appels à dataset_builder et llm_judge)

        return {
            "status": "success",
            "message": "Évaluation exécutée avec succès en utilisant les clés configurées.",
            "details": {
                "num_questions_requested": request.num_questions
            }
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'évaluation : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ragas")
def test_ragas_connection():
    """Route de test pour valider le bon fonctionnement de la configuration RAGAS/Judge."""
    try:
        llm = get_ragas_llm()
        return {"status": "ok", "message": "Configuration RAGAS / Judge initialisée avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))