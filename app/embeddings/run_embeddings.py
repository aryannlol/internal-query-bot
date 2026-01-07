# app/embeddings/run_embeddings.py
from app.ingestion.ingest import run_ingestion
from app.embeddings.embedder import Embedder

def run_embeddings():
    """
    Runs ingestion and generates embeddings for all chunks.
    Returns embedded data.
    """
    chunks = run_ingestion()
    embedder = Embedder()
    data = embedder.embed_chunks(chunks)

    print("Embedding shape:", data["vectors"].shape)
    return data

if __name__ == "__main__":
    run_embeddings()