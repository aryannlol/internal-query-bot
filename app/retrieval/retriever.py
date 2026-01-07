from app.vectorstore.chroma_store import ChromaStore
from app.embeddings.embedder import Embedder
from app.config import settings

class Retriever:
    def __init__(self):
        # ✅ Use the SHARED ChromaStore instance
        self.store = ChromaStore()
        self.embedder = Embedder()

    def retrieve(self, question: str):
        print(f"\n--- 🚀 Starting Retrieval for: '{question}' ---")
        
        query_vec = self.embedder.embed_query(question)
        
        # 1. Check count
        count = self.store.collection.count()
        print(f"DEBUG: Total documents in Vector Store: {count}")
        
        if count == 0:
            print("⚠️ Index is empty.")
            return []

        # 2. Safety: Don't ask for more than we have
        requested_k = min(settings.top_k, count)

        try:
            # 3. Perform the search
            results = self.store.query(query_vec, top_k=requested_k)
            
            docs = results.get("documents", [[]])[0]
            metas = results.get("metadatas", [[]])[0]
            dists = results.get("distances", [[]])[0]

            print(f"DEBUG: Chroma returned {len(docs)} raw matches.")

            chunks = []
            for i, (doc, meta, dist) in enumerate(zip(docs, metas, dists)):
                status = "✅ ACCEPTED" if dist < settings.distance_threshold else "❌ REJECTED (Too far)"
                
                # Debug print for every single chunk returned by Chroma
                print(f"\n  Chunk #{i+1} | Score: {dist:.4f} | {status}")
                print(f"  Source: {meta.get('source')}")
                print(f"  Snippet: {doc[:100].replace('\\n', ' ')}...")

                if dist < settings.distance_threshold:
                    chunks.append({
                        "content": doc,
                        "source": meta.get("source"),
                        "score": dist
                    })
            
            print(f"\n--- 🎯 Final Result: Sent {len(chunks)} chunks to LLM ---\n")
            return chunks

        except Exception as e:
            print(f"❌ Query error: {e}")
            import traceback
            traceback.print_exc()
            return []