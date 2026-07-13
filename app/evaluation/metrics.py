import re

def _tokenize(text: str) -> set:
    return set(re.findall(r"\w+", text.lower()))

def context_precision_score(retrieved_context: str, ground_truth: str) -> float:
    """Proportion des mots-clés de la vérité terrain retrouvés dans le contexte récupéré."""
    gt_tokens = _tokenize(ground_truth)
    context_tokens = _tokenize(retrieved_context)
    if not gt_tokens:
        return 0.0
    overlap = gt_tokens & context_tokens
    return round(len(overlap) / len(gt_tokens), 3)

def context_recall_score(generated_answer: str, ground_truth: str) -> float:
    """Proportion des mots-clés de la vérité terrain retrouvés dans la réponse générée."""
    gt_tokens = _tokenize(ground_truth)
    answer_tokens = _tokenize(generated_answer)
    if not gt_tokens:
        return 0.0
    overlap = gt_tokens & answer_tokens
    return round(len(overlap) / len(gt_tokens), 3)