
# 📚 Internal Query Bot

An **internal knowledge base question–answering system** built with **FastAPI, ChromaDB, and React**.
Designed to ingest company documents (policies, guides, manuals) and allow users to **ask natural-language questions** with accurate, source-grounded answers.

This project includes:

* Incremental document ingestion (no full reindex)
* Vector-based semantic search
* Admin dashboard for document management
* Clean backend/frontend separation

---

## 🚀 Features

### 🔍 Intelligent Q&A

* Semantic search using embeddings
* Context-aware answer generation
* Source attribution for answers

### 📂 Document Management (Admin)

* Upload documents incrementally (`.md` for better search)
* Skip duplicates automatically
* Delete documents with vector cleanup
* Live preview of documents

### ⚡ Efficient Architecture

* ChromaDB for vector storage
* No full rebuild on every upload
* Modular, testable backend design

### 🖥️ Admin Dashboard (React)

* Upload, view, and delete documents
* Markdown preview
* Clean, minimal UI

---

## 🧠 High-Level Architecture

```
User Question
     ↓
Retriever (ChromaDB vector search)
     ↓
Relevant Chunks
     ↓
Answer Generator (LLM)
     ↓
Final Answer + Sources
```

Admin Flow:

```
Upload → Chunk → Embed → Store (incremental)
Delete → Remove chunks → Sync index
```

---

## 📁 Project Structure

```
internal-query-bot/
├── app/                # FastAPI backend
│   ├── admin/          # Admin pipelines
│   ├── embeddings/     # Embedding logic
│   ├── generation/     # Answer generation
│   ├── ingestion/      # Loaders & chunking
│   ├── retrieval/      # Vector retrieval
│   ├── vectorstore/    # ChromaDB wrapper
│   └── main.py         # App entry point
│
├── data/
│   └── documents/      # Source knowledge files
│
├── frontend/           # React admin dashboard
│   ├── src/
│   └── vite.config.js
│
├── requirements.txt
├── readme.md

```

> ⚠️ Runtime artifacts (`.venv`, `.chroma`, `node_modules`) are intentionally ignored via `.gitignore`.

---

## 🛠️ Tech Stack

### Backend

* **FastAPI**
* **ChromaDB**
* **Python**
* **Pydantic**
* **Uvicorn**

### Frontend

* **React**
* **Vite**
* **Lucide Icons**
* **React Markdown**

---

## ⚙️ Setup Instructions

### 1️⃣ Backend Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://localhost:8000
```

---

### 2️⃣ Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 📄 Supported Documents

* `.md` (Markdown)

Documents are stored in:

```
data/documents/
```

---

## 🔐 Admin Capabilities

* Incremental document upload
* Vector-safe deletion
* Live preview
* Rate-limited admin endpoints

(Admin auth can be added later.)

---

## 🧪 Current Status

* ✅ Core ingestion & retrieval complete
* ✅ Admin dashboard functional
* ✅ Incremental indexing implemented
* ⏳ Authentication (planned)
* ⏳ Dockerization (planned)

---

## 📌 Future Improvements

* Role-based access control
* Background ingestion jobs
* File content hashing (dedup by content)
* Docker + CI pipeline
* Usage analytics
* Text to markdown
---


Built by **Aryan**

---
