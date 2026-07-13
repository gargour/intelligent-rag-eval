from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import init_db
from app.api.routes import documents, chat, evaluation, health

app = FastAPI(
    title="AI Research Assistant API",
    description="RAG-based document Q&A system with FAISS + Grok",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(chat.router)
app.include_router(evaluation.router)

@app.on_event("startup")
def on_startup():
    init_db()