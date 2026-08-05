from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_type: str
    upload_date: datetime
    num_pages: int
    num_chunks: int
    status: str

    model_config = {"from_attributes": True}

class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    message: str