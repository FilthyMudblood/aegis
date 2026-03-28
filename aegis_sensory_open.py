def calculate_fact_error_x(draft_output: str, rag_context: str) -> float:
    """
    Open-reference factual tension score: word-level Jaccard distance vs RAG context.
    """
    if not rag_context or not draft_output:
        return 1.0
    a = set((draft_output or "").lower().split())
    b = set((rag_context or "").lower().split())
    if not a:
        return 0.0
    inter = len(a & b)
    union = len(a | b) or 1
    overlap = inter / union
    return round(max(0.0, min(1.0, 1.0 - overlap)), 3)
