def enrich_metadata(chunk, document_id: str, filename: str):
    """Ajoute des métadonnées enrichies utiles pour les citations."""
    chunk.metadata["document_id"] = document_id
    chunk.metadata["filename"] = filename

    # Heuristique simple pour détecter un titre de section
    first_line = chunk.page_content.strip().split("\n")[0]
    if len(first_line) < 80 and first_line.isupper():
        chunk.metadata["section_title"] = first_line

    return chunk