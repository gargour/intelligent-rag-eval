from app.vectorstore.faiss_store import get_vectorstore
from app.config import get_settings

settings = get_settings()

def retrieve_relevant_chunks(query: str, document_ids: list = None, top_k: int = None):
    vectorstore = get_vectorstore()
    top_k = top_k or settings.top_k_retrieval

    filter_dict = None
    if document_ids:
        filter_dict = {"document_id": {"$in": document_ids}}

    return vectorstore.similarity_search_with_relevance_scores(
        query, k=top_k, filter=filter_dict
    )