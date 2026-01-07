from sentence_transformers import SentenceTransformer
from app.config import settings

_model = None

class Embedder:
    def __init__(self):
        global _model
        if _model is None:
            _model = SentenceTransformer(settings.embedding_model)
        self.model = _model

    # ✅ ENSURE THIS NAME MATCHES EXACTLY
    def embed_chunks(self, chunks):
        print('before embed chunk')
        texts = [c["text"] for c in chunks] # Use "text" here as we discussed
        vectors = self.model.encode(texts)
        print('after vector ',vectors)
        return {
            "chunks": chunks,
            "vectors": vectors

        }

    def embed_query(self, query: str):
        return self.model.encode(query)