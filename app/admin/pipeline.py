from app.ingestion.ingest import run_ingestion
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore

def rebuild_pipeline():
    """
    Rebuild the entire vector index from scratch.
    Reads all documents from disk and re-indexes them.
    """
    print("Starting ingestion...")
    chunks = run_ingestion()

    print("Running embeddings...")
    embedder = Embedder()
    data = embedder.embed_chunks(chunks)

    print("Building vector index...")
    # ✅ Use the SHARED ChromaStore instance
    store = ChromaStore()
    store.rebuild(
        chunks=data["chunks"],
        embeddings=data["vectors"]
    )
    print("after rebuild")

    print(f"Pipeline rebuild completed. Total indexed: {store.collection.count()}")