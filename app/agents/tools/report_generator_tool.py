from app.vectorstore.retriever import retrieve_relevant_chunks
from app.llm.factory import get_llm_client
from app.llm.prompt_templates.report_prompt import REPORT_SYSTEM_PROMPT, build_report_prompt

def generate_report_tool(topic: str, document_ids: list = None, top_k: int = 15):
    results = retrieve_relevant_chunks(topic, document_ids=document_ids, top_k=top_k)
    chunks = [r[0] for r in results]

    if not chunks:
        return "Aucune information trouvée pour générer le rapport."

    prompt = build_report_prompt(chunks, topic)
    llm = get_llm_client()
    return llm.generate(REPORT_SYSTEM_PROMPT, prompt)