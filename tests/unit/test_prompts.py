from langchain.schema import Document as LCDocument
from app.llm.prompt_templates.qa_prompt import build_qa_prompt

def test_build_qa_prompt_includes_context_and_question():
    chunks = [LCDocument(page_content="Contenu test", metadata={"filename": "doc.pdf", "page": 1})]
    prompt = build_qa_prompt("Quelle est la conclusion ?", chunks)
    assert "Contenu test" in prompt
    assert "Quelle est la conclusion ?" in prompt
    assert "doc.pdf" in prompt