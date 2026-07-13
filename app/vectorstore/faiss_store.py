from pathlib import Path
from langchain_community.vectorstores import FAISS
from app.embeddings.embedder import get_embedder
from app.config import get_settings

settings = get_settings()
_vectorstore_instance = None

INDEX_PATH = Path(settings.faiss_index_dir)
INDEX_PATH.mkdir(parents=True, exist_ok=True)


def _load_index_if_exists():
    embedder = get_embedder()
    index_file = INDEX_PATH / "index.faiss"
    if index_file.exists():
        return FAISS.load_local(
            str(INDEX_PATH), embedder, allow_dangerous_deserialization=True
        )
    return None


class FaissVectorStore:
    def __init__(self):
        self.store = _load_index_if_exists()

    def add_documents(self, documents: list) -> list[str]:
        if not documents:
            return []

        if self.store is None:
            self.store = FAISS.from_documents(documents, get_embedder())
        else:
            self.store.add_documents(documents)

        self._persist()

        ids = list(self.store.docstore._dict.keys())[-len(documents):]
        return ids

    def similarity_search_with_relevance_scores(self, query: str, k: int = 5, filter: dict = None):
        if self.store is None:
            return []

        oversample = k * 3 if filter else k
        results = self.store.similarity_search_with_relevance_scores(query, k=oversample)

        if filter and "document_id" in filter:
            allowed_ids = set(filter["document_id"].get("$in", []))
            results = [
                (doc, score) for doc, score in results
                if doc.metadata.get("document_id") in allowed_ids
            ][:k]
        else:
            results = results[:k]

        return results

    def delete_by_document_id(self, document_id: str):
        if self.store is None:
            return
        ids_to_delete = [
            doc_id for doc_id, doc in self.store.docstore._dict.items()
            if doc.metadata.get("document_id") == document_id
        ]
        if ids_to_delete:
            self.store.delete(ids_to_delete)
            self._persist()

    def _persist(self):
        self.store.save_local(str(INDEX_PATH))


def get_vectorstore() -> FaissVectorStore:
    global _vectorstore_instance
    if _vectorstore_instance is None:
        _vectorstore_instance = FaissVectorStore()
    return _vectorstore_instance