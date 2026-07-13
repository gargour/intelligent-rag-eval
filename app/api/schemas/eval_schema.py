from pydantic import BaseModel
from typing import Optional

class EvalRunRequest(BaseModel):
    num_questions_per_doc: int = 3
    document_ids: Optional[list[str]] = None

class EvalMetricResult(BaseModel):
    question: str
    generated_answer: str
    ground_truth: Optional[str]
    faithfulness: float
    answer_relevance: float
    context_precision: float
    context_recall: float

class EvalRunResponse(BaseModel):
    total_questions: int
    avg_faithfulness: float
    avg_answer_relevance: float
    avg_context_precision: float
    avg_context_recall: float
    details: list[EvalMetricResult]