# SentenceTransformers converts text → vector embeddings
from sentence_transformers import SentenceTransformer

# Load embedding model once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    # Convert list of texts into embeddings (vectors)
    return model.encode(texts, show_progress_bar=True)

def embed_query(query):
    # Convert a single query into embedding
    return model.encode([query])[0]  # [0] because output is a list