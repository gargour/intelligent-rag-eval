from app.rag.chain import run_rag_query

def search_documents_tool(question: str, document_ids: list = None):
    return run_rag_query(question, document_ids=document_ids)