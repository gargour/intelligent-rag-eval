from unittest.mock import patch

@patch("app.rag.chain.retrieve_relevant_chunks")
@patch("app.rag.chain.get_llm_client")
def test_run_rag_query_no_results(mock_llm, mock_retrieve):
    from app.rag.chain import run_rag_query

    mock_retrieve.return_value = []
    result = run_rag_query("question sans réponse")

    assert "Aucune information" in result.answer
    assert result.citations == []