"""Vérifie que tous les fichiers attendus du projet existent."""
from pathlib import Path

expected_files = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/dependencies.py",

    "app/core/__init__.py",
    "app/core/security.py",
    "app/core/logging.py",
    "app/core/exceptions.py",

    "app/api/__init__.py",
    "app/api/routes/__init__.py",
    "app/api/routes/documents.py",
    "app/api/routes/chat.py",
    "app/api/routes/evaluation.py",
    "app/api/routes/health.py",
    "app/api/schemas/__init__.py",
    "app/api/schemas/document_schema.py",
    "app/api/schemas/chat_schema.py",
    "app/api/schemas/eval_schema.py",

    "app/ingestion/__init__.py",
    "app/ingestion/loaders.py",
    "app/ingestion/chunking.py",
    "app/ingestion/metadata_extractor.py",
    "app/ingestion/pipeline.py",

    "app/embeddings/__init__.py",
    "app/embeddings/embedder.py",
    "app/embeddings/cache.py",

    "app/vectorstore/__init__.py",
    "app/vectorstore/base.py",
    "app/vectorstore/faiss_store.py",
    "app/vectorstore/retriever.py",

    "app/llm/__init__.py",
    "app/llm/base.py",
    "app/llm/grok_client.py",
    "app/llm/factory.py",
    "app/llm/prompt_templates/__init__.py",
    "app/llm/prompt_templates/qa_prompt.py",
    "app/llm/prompt_templates/summarize_prompt.py",
    "app/llm/prompt_templates/compare_prompt.py",
    "app/llm/prompt_templates/report_prompt.py",

    "app/rag/__init__.py",
    "app/rag/chain.py",
    "app/rag/citation_builder.py",
    "app/rag/reranker.py",

    "app/agents/__init__.py",
    "app/agents/agent_router.py",
    "app/agents/memory.py",
    "app/agents/tools/__init__.py",
    "app/agents/tools/search_tool.py",
    "app/agents/tools/summarizer_tool.py",
    "app/agents/tools/comparator_tool.py",
    "app/agents/tools/report_generator_tool.py",

    "app/evaluation/__init__.py",
    "app/evaluation/metrics.py",
    "app/evaluation/ragas_eval.py",
    "app/evaluation/llm_judge.py",
    "app/evaluation/dataset_builder.py",

    "app/db/__init__.py",
    "app/db/models.py",
    "app/db/session.py",

    "frontend/Home.py",
    "frontend/utils/api_client.py",
    "frontend/pages/1_Upload_Documents.py",
    "frontend/pages/2_Chat_Assistant.py",
    "frontend/pages/3_Compare_Documents.py",
    "frontend/pages/4_Generate_Report.py",
    "frontend/pages/5_Evaluation_Dashboard.py",

    "scripts/ingest_documents.py",
    "scripts/run_evaluation.py",
    "scripts/seed_db.py",

    ".env",
    "requirements.txt",
    "docker-compose.yml",
]

missing = []
present = []

for f in expected_files:
    if Path(f).exists():
        present.append(f)
    else:
        missing.append(f)

print(f"\n✅ Fichiers présents: {len(present)}/{len(expected_files)}\n")

if missing:
    print(f"❌ Fichiers MANQUANTS ({len(missing)}):\n")
    for f in missing:
        print(f"   - {f}")
else:
    print("🎉 Tous les fichiers attendus sont présents !")