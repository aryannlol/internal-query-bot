from app.ingestion.ingest import run_ingestion
from app.embeddings.embedder import Embedder
from app.vectorstore.chroma_store import ChromaStore

def build_vector_store():
    chunks = run_ingestion()

    embedder = Embedder()
    data = embedder.embed_chunks(chunks)
    

    store = ChromaStore()
    print('before rebuild')
    store.build(
        chunks=data["chunks"],
        embeddings=data["vectors"]
    )
    print('after rebuild')

if __name__ == "__main__":
    build_vector_store()