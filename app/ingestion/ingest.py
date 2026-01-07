# app/ingestion/ingest.py
from app.ingestion.loader import load_documents
from app.ingestion.chunker import create_chunks

def run_ingestion():
    docs = load_documents("data/documents")
    chunks = create_chunks(docs)

    print(f"Loaded {len(docs)} documents")
    print(f"Created {len(chunks)} chunks")

    return chunks

if __name__ == "__main__":
    run_ingestion()