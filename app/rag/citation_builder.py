from app.api.schemas.chat_schema import Citation

def build_citations(retrieved_chunks_with_scores) -> list[Citation]:
    citations = []
    for chunk, score in retrieved_chunks_with_scores:
        citations.append(Citation(
            document_id=chunk.metadata.get("document_id", ""),
            filename=chunk.metadata.get("filename", "unknown"),
            page_number=chunk.metadata.get("page"),
            section_title=chunk.metadata.get("section_title"),
            snippet=chunk.page_content[:250] + "...",
            relevance_score=round(float(score), 3),
        ))
    return citations