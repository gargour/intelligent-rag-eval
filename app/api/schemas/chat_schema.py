from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    document_ids: Optional[List[str]] = None
    mode: str = "qa"  # qa | summarize | compare | report
    top_k: int = 5

class Citation(BaseModel):
    document_id: str
    filename: str
    page_number: Optional[int]
    section_title: Optional[str]
    snippet: str
    relevance_score: float

class AnswerResponse(BaseModel):
    answer: str
    citations: List[Citation]
    latency_ms: int