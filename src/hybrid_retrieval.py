import random
from rank_bm25 import BM25Okapi


def hybrid_mock_retrieve(query, chunks, top_k=5, alpha=0.9):
    """
    Hybrid retrieval using:
    - BM25 (real lexical search)
    - Mock semantic score (random)

    Args:
        query: user query string
        chunks: list of chunk dicts
        top_k: number of results to return
        alpha: weight for BM25 score (0 to 1, where 1 = only BM25, 0 = only semantic)

    Returns:
        List of ranked chunks with score breakdown
    """

    corpus = [chunk["content"] for chunk in chunks]
    tokenized_corpus = [doc.lower().split() for doc in corpus]

    bm25 = BM25Okapi(tokenized_corpus)

    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)

    # Normalizing BM25 scores to 0-1 range
    max_bm25 = max(bm25_scores)
    min_bm25 = min(bm25_scores)

    def normalize(score):
        if max_bm25 == min_bm25:
            return 0.0
        return (score - min_bm25) / (max_bm25 - min_bm25)

    results = []

    for i, chunk in enumerate(chunks):
        bm25_raw = bm25_scores[i]
        bm25_norm = float(normalize(bm25_raw))

        # Simulating semantic score with a random value (replace this with LLM inference in a real implementation)
        semantic_score = random.uniform(0, 1)

        final_score = alpha * bm25_norm + (1 - alpha) * semantic_score

        results.append(
            {
                "chunk": chunk,
                "bm25_score": bm25_norm,
                "semantic_score": semantic_score,
                "final_score": final_score,
            }
        )

    ranked = sorted(results, key=lambda x: x["final_score"], reverse=True)

    return ranked[:top_k]
