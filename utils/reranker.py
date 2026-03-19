from sentence_transformers import CrossEncoder

# Cross-encoder model (more accurate than embeddings)
models = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, results, top_k=3):
    """
    Re-rank retrieved chunks based on relevance to query.
    """

    if not results:
        return results

    # Prepare pairs: (query, chunk_text)
    pairs = [(query, r["text"]) for r in results]

    # Get relevance scores
    scores = models.predict(pairs)

    # Attach scores
    scored_results = []
    for i, r in enumerate(results):
        scored_results.append({
            "text": r["text"],
            "metadata": r["metadata"],
            "score": scores[i]
        })

    # Sort by score (descending)
    scored_results = sorted(scored_results, key=lambda x: x["score"], reverse=True)

    # Return top-k
    return scored_results[:top_k]