# Import all modules we created
from utils.pdf_loader import load_pdf
from utils.text_cleaner import clean_text
from utils.chunker import chunk_text
from utils.embedder import embed_texts, embed_query
from utils.vector_store import VectorStore
from utils.llm import generate_answer
from utils.memory import ChatMemory
from utils.query_rewriter import rewrite_query
from utils.reranker import rerank


def ingest_pdf(file_path):
    # Step 1: Load PDF
    pages = load_pdf(file_path)

    # Step 2: Clean text on each page
    for page in pages:
        page["text"] = clean_text(page["text"])

    # Step 3: Split into chunks
    chunks = chunk_text(pages)

    return chunks


def build_index(chunks):
    # Extract only text content from chunks
    texts = [chunk["content"] for chunk in chunks]

    # Extract metadata (page numbers)
    metadata = [{"page": chunk["page"]} for chunk in chunks]

    # Convert text into embeddings
    embeddings = embed_texts(texts)

    # Determine embedding dimension (e.g., 384)
    dim = len(embeddings[0])

    # Initialize vector store
    store = VectorStore(dim)

    # Add embeddings + text + metadata to FAISS
    store.add(embeddings, texts, metadata)

    return store


def format_context(results):
    context = ""

    for r in results:
        context += f"(Page {r['metadata']['page']}): {r['text']}\n\n"

    return context


if __name__ == "__main__":

    pdf_path = "Resume.pdf"

    print("📄 Ingesting document...")
    chunks = ingest_pdf(pdf_path)

    print("🔍 Building index...")
    store = build_index(chunks)

    print("🧠 Initializing memory...")
    memory = ChatMemory()

    print("\n🤖 Chat system ready! Type 'exit' to quit.\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            print("👋 Exiting...")
            break

        # 🔁 Step 1: Rewrite query (memory-aware)
        rewritten_query = rewrite_query(query, memory)

        # 🔍 Step 2: Retrieve relevant chunks
        query_embedding = embed_query(rewritten_query)
        
        results = store.search(query_embedding, k=8)

        results = rerank(rewritten_query, results, top_k=3)

        # 📄 Step 3: Format context
        context = format_context(results)

        # 🤖 Step 4: Generate answer
        answer = generate_answer(context, query, memory)

        print("\n🤖 Answer:\n", answer)