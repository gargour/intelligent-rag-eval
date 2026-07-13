from sentence_transformers import CrossEncoder

_reranker = None

def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _reranker

def rerank(query: str, results: list, top_k: int = 5):
    """results: list de (Document, score) issus de la recherche vectorielle."""
    if not results:
        return results

    reranker = get_reranker()
    pairs = [[query, doc.page_content] for doc, _ in results]
    scores = reranker.predict(pairs)

    reranked = sorted(zip([r[0] for r in results], scores), key=lambda x: x[1], reverse=True)
    return reranked[:top_k]