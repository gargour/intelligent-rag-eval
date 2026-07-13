from app.ingestion.loaders import load_document
from app.ingestion.chunking import split_documents
from app.ingestion.metadata_extractor import enrich_metadata
from app.vectorstore.faiss_store import get_vectorstore
from app.db.models import Document, Chunk
from app.db.session import SessionLocal
import uuid

def ingest_document(file_path: str, filename: str, file_type: str) -> str:
    db = SessionLocal()
    doc_record = Document(
        id=str(uuid.uuid4()),
        filename=filename,
        file_type=file_type,
        status="processing",
    )
    db.add(doc_record)
    db.commit()

    try:
        raw_docs = load_document(file_path)
        chunks = split_documents(raw_docs)

        for c in chunks:
            enrich_metadata(c, doc_record.id, filename)

        vectorstore = get_vectorstore()
        vector_ids = vectorstore.add_documents(chunks)

        for chunk, vid in zip(chunks, vector_ids):
            chunk_record = Chunk(
                id=str(uuid.uuid4()),
                document_id=doc_record.id,
                content=chunk.page_content,
                page_number=chunk.metadata.get("page"),
                section_title=chunk.metadata.get("section_title"),
                chunk_index=chunk.metadata.get("chunk_index"),
                vector_id=vid,
            )
            db.add(chunk_record)

        doc_record.num_pages = len(raw_docs)
        doc_record.num_chunks = len(chunks)
        doc_record.status = "ready"
        db.commit()
        return doc_record.id

    except Exception as e:
        doc_record.status = "failed"
        db.commit()
        raise e
    finally:
        db.close()