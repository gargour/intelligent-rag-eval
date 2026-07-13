from abc import ABC, abstractmethod

class BaseVectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: list) -> list[str]:
        ...

    @abstractmethod
    def similarity_search_with_relevance_scores(self, query: str, k: int, filter: dict = None):
        ...

    @abstractmethod
    def delete_by_document_id(self, document_id: str):
        ...