from unittest.mock import patch, MagicMock

@patch("app.vectorstore.retriever.get_vectorstore")
def test_retrieve_relevant_chunks_calls_vectorstore(mock_get_vs):
    from app.vectorstore.retriever import retrieve_relevant_chunks

    mock_store = MagicMock()
    mock_store.similarity_search_with_relevance_scores.return_value = []
    mock_get_vs.return_value = mock_store

    result = retrieve_relevant_chunks("test query", top_k=3)
    assert result == []
    mock_store.similarity_search_with_relevance_scores.assert_called_once()