class DocumentNotFoundError(Exception):
    pass

class IngestionError(Exception):
    pass

class RetrievalError(Exception):
    pass

class LLMGenerationError(Exception):
    pass