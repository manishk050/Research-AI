import streamlit as st

from utils.pdf_loader import load_pdf
from utils.text_cleaner import clean_text
from utils.chunker import chunk_text
from utils.embedder import embed_texts, embed_query
from utils.vector_store import VectorStore
from utils.memory import ChatMemory
from utils.llm import generate_answer
from utils.query_rewriter import rewrite_query
from utils.reranker import rerank


# -------------------------------
# Helper Functions
# -------------------------------
def ingest_pdf(file):
    pages = load_pdf(file)

    for page in pages:
        page["text"] = clean_text(page["text"])

    return chunk_text(pages)


def build_index(chunks):
    texts = [c["content"] for c in chunks]
    metadata = [{"page": c["page"]} for c in chunks]

    embeddings = embed_texts(texts)

    store = VectorStore(len(embeddings[0]))
    store.add(embeddings, texts, metadata)

    return store


def format_context(results):
    context = ""
    for r in results:
        context += f"(Page {r['metadata']['page']}): {r['text']}\n\n"
    return context


# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="AI Research Copilot", layout="wide")

st.title("🤖 AI Research Copilot")

# Session state (IMPORTANT)
if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory()

if "store" not in st.session_state:
    st.session_state.store = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    st.success("PDF uploaded successfully!")

    if st.session_state.store is None:
        with st.spinner("Processing PDF..."):
            chunks = ingest_pdf(uploaded_file)
            st.session_state.store = build_index(chunks)

        st.success("Document indexed!")


# -------------------------------
# Chat Interface
# -------------------------------
if st.session_state.store:

    user_input = st.chat_input("Ask a question...")

    if user_input:

        # Save user message
        st.session_state.chat_history.append(("user", user_input))

        # 🔁 Rewrite query
        rewritten_query = rewrite_query(user_input, st.session_state.memory)

        # 🔍 Retrieve
        query_embedding = embed_query(rewritten_query)
        results = st.session_state.store.search(query_embedding, k=8)

        # 🔥 Rerank
        results = rerank(rewritten_query, results, top_k=3)

        # 📄 Context
        context = format_context(results)

        # 🤖 Generate answer
        answer = generate_answer(context, user_input, st.session_state.memory)

        # Save response
        st.session_state.chat_history.append(("assistant", answer))


# -------------------------------
# Display Chat
# -------------------------------
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)