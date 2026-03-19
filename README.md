# 🤖 AI Research Copilot (Conversational RAG System)

An end-to-end **AI-powered document question-answering system** that allows users to upload PDFs and interact with them conversationally.

This project implements a **production-style Retrieval-Augmented Generation (RAG) pipeline** with memory, query rewriting, reranking, and a Streamlit UI.

---

## 🚀 Features

- 📄 **PDF Ingestion** – Upload and process documents
- 🔍 **Semantic Search (FAISS)** – Retrieve relevant chunks using embeddings
- 🧠 **Conversational Memory** – Supports multi-turn conversations
- 🔁 **Query Rewriting** – Improves retrieval using chat history
- 🎯 **Reranking (Cross-Encoder)** – Enhances relevance of retrieved results
- 🤖 **LLM Integration (Hugging Face)** – Generates grounded answers
- 💬 **Streamlit Chat UI** – Clean, interactive interface

---

## 🧠 System Architecture

```
User Query
   ↓
Query Rewriting (memory-aware)
   ↓
FAISS Retrieval (top-k)
   ↓
Reranking (CrossEncoder)
   ↓
Context Formatting
   ↓
LLM (Hugging Face)
   ↓
Answer + Memory Update
```

---

## 📂 Project Structure

```
project/
│── app.py                # Streamlit UI
│── ingest.py             # Main pipeline (CLI version)
│
├── utils/
│   ├── pdf_loader.py
│   ├── text_cleaner.py
│   ├── chunker.py
│   ├── embedder.py
│   ├── vector_store.py
│   ├── memory.py
│   ├── llm.py
│   ├── query_rewriter.py
│   └── reranker.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-research-copilot.git
cd ai-research-copilot
```

---

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit pymupdf sentence-transformers faiss-cpu requests
```

---

## 🔑 Hugging Face API Setup (IMPORTANT)

This project uses **Hugging Face Inference API** for LLM responses.

👉 You MUST use your own access token.

### Steps:

1. Go to: https://huggingface.co/settings/tokens  
2. Create a **Read Token**
3. Open:

```
utils/llm.py
```

4. Replace:

```python
headers = {
    "Authorization": "Bearer YOUR_HF_TOKEN"
}
```

⚠️ Without this, the LLM will NOT work.

---

## ▶️ Run the Application

### 🔹 Streamlit UI

```bash
streamlit run app.py
```

---

### 🔹 CLI Version (Optional)

```bash
python ingest.py
```

---

## 💬 Example Usage

1. Upload a PDF  
2. Ask questions like:
   - "What are the key skills mentioned?"
   - "What experience does the candidate have?"
   - "What about machine learning?"

3. Follow up naturally:
   - "What about automation?"
   - "Any cloud experience?"

---

## 🧠 Key Technologies

- **SentenceTransformers** – Embeddings
- **FAISS** – Vector search
- **CrossEncoder** – Reranking
- **Hugging Face API** – LLM inference
- **Streamlit** – UI

---

## 🔥 What Makes This Project Special

- ✅ Not just basic RAG — includes **memory + rewriting + reranking**
- ✅ Modular architecture (production-style)
- ✅ No heavy frameworks (minimal dependencies)
- ✅ Fully customizable pipeline

---

## ⚠️ Limitations

- Depends on Hugging Face free API (rate limits possible)
- Short-term memory only
- No persistent vector DB (in-memory FAISS)

---

## 🚀 Future Improvements

- [ ] Multi-document support  
- [ ] Streaming responses (real-time typing)  
- [ ] Source highlighting in UI  
- [ ] Hybrid search (keyword + semantic)  
- [ ] Deployment (Docker / Cloud)

---

## 👨‍💻 Author

Built as part of preparation for an **AI Engineer role**.

---

## ⭐ If You Like This Project

Give it a ⭐ on GitHub — it helps!
