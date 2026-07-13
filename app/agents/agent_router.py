from app.agents.tools.search_tool import search_documents_tool
from app.agents.tools.summarizer_tool import summarize_document_tool
from app.agents.tools.comparator_tool import compare_documents_tool
from app.agents.tools.report_generator_tool import generate_report_tool

def route_request(mode: str, **kwargs):
    """
    mode: qa | summarize | compare | report
    kwargs attendus selon le mode:
      - qa: question, document_ids
      - summarize: document_id
      - compare: document_id_a, document_id_b, question
      - report: topic, document_ids
    """
    if mode == "qa":
        return search_documents_tool(kwargs["question"], kwargs.get("document_ids"))
    elif mode == "summarize":
        return summarize_document_tool(kwargs["document_id"])
    elif mode == "compare":
        return compare_documents_tool(
            kwargs["document_id_a"], kwargs["document_id_b"], kwargs["question"]
        )
    elif mode == "report":
        return generate_report_tool(kwargs["topic"], kwargs.get("document_ids"))
    else:
        raise ValueError(f"Mode inconnu: {mode}")
