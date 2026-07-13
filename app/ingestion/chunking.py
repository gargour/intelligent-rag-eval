from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.config import get_settings

settings = get_settings()

def split_documents(documents, chunk_size=None, chunk_overlap=None):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size or settings.chunk_size,
        chunk_overlap=chunk_overlap or settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)

    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i

    return chunks