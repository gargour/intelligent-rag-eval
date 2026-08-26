from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base = declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=gen_uuid)
    filename = Column(String, nullable=False)
    file_type = Column(String)
    upload_date = Column(DateTime, default=datetime.utcnow)
    num_pages = Column(Integer, default=0)
    num_chunks = Column(Integer, default=0)
    status = Column(String, default="processing")

    chunks = relationship("Chunk", back_populates="document", cascade="all, delete")


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(String, primary_key=True, default=gen_uuid)
    document_id = Column(String, ForeignKey("documents.id"))
    content = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    section_title = Column(String, nullable=True)
    chunk_index = Column(Integer)
    vector_id = Column(String)

    document = relationship("Document", back_populates="chunks")


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(String, primary_key=True, default=gen_uuid)
    question = Column(Text)
    answer = Column(Text)
    citations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    latency_ms = Column(Integer)


class EvalResult(Base):
    __tablename__ = "eval_results"

    id = Column(String, primary_key=True, default=gen_uuid)
    question = Column(Text)
    generated_answer = Column(Text)
    ground_truth = Column(Text, nullable=True)
    faithfulness = Column(Float)
    answer_relevance = Column(Float)
    context_precision = Column(Float)
    context_recall = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

# --- Ajout pour l'historique des évaluations ---
class EvaluationResultModel(Base):
    __tablename__ = "evaluation_results"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_name = Column(String, index=True)
    faithfulness = Column(Float)
    relevance = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    