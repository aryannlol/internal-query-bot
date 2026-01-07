import chromadb
from chromadb.config import Settings as ChromaSettings
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# ✅ CRITICAL: Global singleton to prevent recreation
_chroma_instance = None

class ChromaStore:
    def __init__(self):
        global _chroma_instance

        if _chroma_instance is None:
            logger.info("Creating NEW ChromaDB client (IN-MEMORY)")

            self.client = chromadb.Client(
                ChromaSettings(
                    chroma_db_impl="duckdb",
                    anonymized_telemetry=False
                )
            )

            self.collection = self.client.get_or_create_collection(
                name="internal_docs"
            )

            _chroma_instance = self
        else:
            logger.info("Reusing existing ChromaDB client")
            self.client = _chroma_instance.client
            self.collection = _chroma_instance.collection


    def build(self, chunks, embeddings):
        """Initial build - adds documents to collection"""
        documents = [c["text"] for c in chunks]
        metadatas = [{"source": c["source"]} for c in chunks]
        ids = [f"id_{i}" for i in range(len(chunks))]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(chunks)} documents to index")

    def rebuild(self, chunks, embeddings):
        """Complete rebuild - deletes all and re-adds"""
        global _chroma_instance
        
        try:
            # Delete and recreate collection
            self.client.delete_collection(name="internal_docs")
            logger.info("Deleted old collection")
            
            self.collection = self.client.create_collection(name="internal_docs")
            logger.info("Created new collection")
            
            # Update global reference
            _chroma_instance.collection = self.collection
            
            # Add all documents
            if chunks and len(chunks) > 0:
                documents = [c["text"] for c in chunks]
                metadatas = [{"source": c["source"]} for c in chunks]
                ids = [f"id_{i}" for i in range(len(chunks))]
                
                self.collection.add(
                    documents=documents,
                    embeddings=embeddings.tolist(),
                    metadatas=metadatas,
                    ids=ids
                )
                logger.info(f"Rebuilt index with {len(chunks)} documents")
            else:
                logger.warning("No chunks to add during rebuild")
                
        except Exception as e:
            logger.error(f"Rebuild failed: {e}")
            raise

    def add_documents(self, chunks, embeddings):
        """Incremental add - appends new documents without rebuilding"""
        if not chunks or len(chunks) == 0:
            logger.warning("No chunks to add")
            return
        
        # Get current max ID to avoid collisions
        current_count = self.collection.count()
        
        documents = [c["text"] for c in chunks]
        metadatas = [{"source": c["source"]} for c in chunks]
        ids = [f"id_{current_count + i}" for i in range(len(chunks))]
        
        self.collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Added {len(chunks)} new documents. Total: {self.collection.count()}")

    def delete_by_source(self, source_filename):
        """Delete all chunks from a specific source file"""
        try:
            # Get all IDs with matching source
            results = self.collection.get(
                where={"source": source_filename}
            )
            
            if results and results["ids"]:
                self.collection.delete(ids=results["ids"])
                logger.info(f"Deleted {len(results['ids'])} chunks from {source_filename}")
                return len(results["ids"])
            else:
                logger.warning(f"No chunks found for source: {source_filename}")
                return 0
                
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            raise

    def query(self, query_embedding, top_k):
        """Query the collection"""
        return self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )