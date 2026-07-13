"""Ingestion batch en CLI: python scripts/ingest_documents.py ./data/raw/*.pdf"""
import sys
from pathlib import Path
from app.ingestion.pipeline import ingest_document
from app.db.session import init_db

def main():
    init_db()
    files = sys.argv[1:]
    if not files:
        print("Usage: python scripts/ingest_documents.py fichier1.pdf fichier2.docx ...")
        return

    for file_path in files:
        path = Path(file_path)
        ext = path.suffix.replace(".", "")
        print(f"Ingestion de {path.name}...")
        doc_id = ingest_document(str(path), path.name, ext)
        print(f"-> Document ID: {doc_id}")

if __name__ == "__main__":
    main()