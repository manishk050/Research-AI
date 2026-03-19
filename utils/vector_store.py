import faiss  # Facebook AI Similarity Search (vector DB)
import numpy as np  # For numerical operations

class VectorStore:
    def __init__(self, dim):
        # Create FAISS index using L2 (Euclidean distance)
        self.index = faiss.IndexFlatL2(dim)

        # Store original texts (for retrieval)
        self.texts = []

        # Store metadata (like page numbers)
        self.metadata = []

    def add(self, embeddings, texts, metadata):
        # Convert embeddings to float32 (required by FAISS)
        self.index.add(np.array(embeddings).astype("float32"))

        # Store corresponding texts
        self.texts.extend(texts)

        # Store metadata
        self.metadata.extend(metadata)

    def search(self, query_embedding, k=3):
        # Search for k nearest vectors
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"), k
        )

        results = []

        # Retrieve matching texts + metadata
        for idx in indices[0]:
            results.append({
                "text": self.texts[idx],
                "metadata": self.metadata[idx]
            })

        return results