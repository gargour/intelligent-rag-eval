from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Document
from app.api.schemas.document_schema import DocumentResponse, DocumentUploadResponse
from app.ingestion.pipeline import ingest_document
from app.vectorstore.faiss_store import get_vectorstore
from pathlib import Path
import shutil

router = APIRouter(prefix="/documents", tags=["Documents"])
UPLOAD_DIR = Path("./data/raw")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    ext = file_path.suffix.replace(".", "")
    try:
        doc_id = ingest_document(str(file_path), file.filename, ext)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'ingestion: {str(e)}")

    return DocumentUploadResponse(
        document_id=doc_id,
        filename=file.filename,
        status="ready",
        message="Document ingéré avec succès",
    )

@router.get("/", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).all()

@router.delete("/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    get_vectorstore().delete_by_document_id(document_id)
    db.delete(doc)
    db.commit()
    return {"message": "Document supprimé"}