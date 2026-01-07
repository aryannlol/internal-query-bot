from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from pathlib import Path
from app.retrieval.retriever import Retriever
from app.generation.answer_generator import AnswerGenerator
from app.admin.pipeline import rebuild_pipeline
from app.ingestion.loader import load_documents
from app.ingestion.chunker import create_chunks
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore
import shutil
from fastapi import UploadFile, File
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings

logger = logging.getLogger(__name__)

DOCUMENTS_DIR = settings.documents_dir
router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

# Use the SAME store instance everywhere
retriever = Retriever()
generator = AnswerGenerator()

class ChatMessage(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    question: str
    history: list[ChatMessage] = []

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: str

@router.post("/query", response_model=QueryResponse)
@limiter.limit(settings.query_rate_limit)
async def query(request: Request, req: QueryRequest):
    user_msg = req.question.lower().strip()

    if user_msg in ["hi", "hello", "hey", "greetings"]:
        return QueryResponse(
            answer="Hello! I'm your Internal Assistant. How can I help you today?",
            sources=[],
            confidence="High"
        )

    if user_msg in ["thank you", "thanks", "thx", "thanks!"]:
        return QueryResponse(
            answer="You're very welcome! Let me know if you need anything else regarding our policies or guides.",
            sources=[],
            confidence="High"
        )

    search_query = req.question
    if len(req.question.split()) < 4 and req.history:
        search_query = f"{req.history[-1].content[:50]} {req.question}"

    chunks = retriever.retrieve(search_query)
    result = await generator.generate(req.question, chunks, req.history)
    
    return QueryResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )

@router.get("/health")
def health():
    store = ChromaStore()
    return {
        "status": "ok",
        "indexed_documents": store.collection.count()
    }

@router.get("/")
def root():
    return {
        "message": settings.app_name,
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

@router.post("/admin/upload-incremental")
@limiter.limit(settings.admin_upload_rate_limit)
async def upload_incremental(request: Request, files: list[UploadFile] = File(...)):
    """
    Upload new documents and add them to existing index (FAST).
    Does NOT rebuild the entire index.
    """
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    for file in files:
        # Validate file type
        if not any(file.filename.endswith(ext) for ext in [".md", ".txt", ".pdf"]):
            logger.warning(f"Skipping unsupported file: {file.filename}")
            continue
        
        dest = DOCUMENTS_DIR / file.filename
        
        if dest.exists():
            logger.warning(f"File {file.filename} already exists - skipping")
            continue
        
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved_files.append(str(dest))
    
    if not saved_files:
        return {
            "status": "warning",
            "message": "No new files added (all files already exist or unsupported)"
        }
    
    try:
        # Process only the new files
        new_docs = []
        for filepath in saved_files:
            path = Path(filepath)
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            
            new_docs.append({
                "text": text,
                "source": path.name
            })
        
        # Create chunks and embeddings
        new_chunks = create_chunks(new_docs)
        embedder = Embedder()
        new_embeddings = embedder.embed_chunks(new_chunks)
        print('new embeddings',new_embeddings)
        # ✅ Use the SHARED store instance
        store = ChromaStore()
        store.add_documents(
            chunks=new_embeddings["chunks"],
            embeddings=new_embeddings["vectors"]
        )
        print('after adding documents')
        logger.info(f"Added {len(new_chunks)} chunks from {len(saved_files)} new documents")
        
        return {
            "status": "success",
            "message": f"Added {len(saved_files)} documents incrementally",
            "files_added": [Path(f).name for f in saved_files],
            "chunks_added": len(new_chunks),
            "total_indexed": store.collection.count()
        }
    
    except Exception as e:
        logger.error(f"Incremental upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to add documents: {str(e)}")

@router.post("/admin/upload-and-rebuild")
@limiter.limit(settings.admin_rebuild_rate_limit)
async def upload_and_rebuild(request: Request, files: list[UploadFile] = File(...)):
    """
    Upload documents and rebuild ENTIRE index.
    Use this for initial setup or when you want to replace everything.
    """
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

    uploaded_count = 0
    for file in files:
        if not any(file.filename.endswith(ext) for ext in [".md", ".txt", ".pdf"]):
            logger.warning(f"Skipping unsupported file: {file.filename}")
            continue
        
        dest = DOCUMENTS_DIR / file.filename
        with open(dest, "wb") as f:
            shutil.copyfileobj(file.file, f)
        uploaded_count += 1

    try:
        print("before rebuild")
        rebuild_pipeline()
        print("after rebuild")
        store = ChromaStore()
        return {
            "status": "success",
            "message": f"Uploaded {uploaded_count} documents and rebuilt entire index",
            "total_indexed": store.collection.count()
        }
    except Exception as e:
        logger.error(f"Rebuild failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to rebuild: {str(e)}")

@router.delete("/admin/documents/{filename}")
@limiter.limit("10/hour")
async def delete_document(request: Request, filename: str):
    """
    Delete a document from disk and remove its chunks from the index.
    """
    file_path = DOCUMENTS_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Document {filename} not found")
    
    try:
        # ✅ Delete from vector store FIRST
        store = ChromaStore()
        deleted_chunks = store.delete_by_source(filename)
        
        # Then delete from disk
        file_path.unlink()
        
        logger.info(f"Deleted {filename} ({deleted_chunks} chunks removed)")
        
        return {
            "status": "success",
            "message": f"Deleted {filename}",
            "chunks_removed": deleted_chunks,
            "total_indexed": store.collection.count()
        }
    except Exception as e:
        logger.error(f"Delete failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete: {str(e)}")

@router.get("/admin/documents")
@limiter.limit("30/minute")
async def list_documents(request: Request):
    """List all documents in the system."""
    if not DOCUMENTS_DIR.exists():
        return {"documents": [], "total": 0}
    
    docs = []
    for path in DOCUMENTS_DIR.glob("*"):
        if path.suffix in [".md", ".txt", ".pdf"]:
            docs.append({
                "filename": path.name,
                "size_kb": round(path.stat().st_size / 1024, 2),
                "modified": path.stat().st_mtime
            })
    
    store = ChromaStore()
    return {
        "documents": docs,
        "total": len(docs),
        "indexed_chunks": store.collection.count()
    }

@router.get("/admin/config")
@limiter.limit("10/minute")
async def get_config(request: Request):
    """View current configuration settings."""
    return {
        "app_name": settings.app_name,
        "debug": settings.debug,
        "ollama_model": settings.ollama_model,
        "ollama_url": settings.ollama_url,
        "top_k": settings.top_k,
        "distance_threshold": settings.distance_threshold,
        "max_chunks": settings.max_chunks,
        "chunk_size": settings.chunk_size,
        "chunk_overlap": settings.chunk_overlap,
        "embedding_model": settings.embedding_model,
        "rate_limits": {
            "query": settings.query_rate_limit,
            "upload": settings.admin_upload_rate_limit,
            "rebuild": settings.admin_rebuild_rate_limit
        }
    }