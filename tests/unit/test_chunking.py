from langchain.schema import Document as LCDocument
from app.ingestion.chunking import split_documents

def test_split_documents_creates_chunks():
    docs = [LCDocument(page_content="Ceci est un texte assez long. " * 50, metadata={})]
    chunks = split_documents(docs, chunk_size=200, chunk_overlap=20)
    assert len(chunks) > 1
    assert all("chunk_index" in c.metadata for c in chunks)