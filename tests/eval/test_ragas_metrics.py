def test_evaluation_module_importable():
    """Vérifie simplement que le module RAGAS s'importe sans erreur d'environnement."""
    from app.evaluation import ragas_eval
    assert hasattr(ragas_eval, "evaluate_rag_dataset")