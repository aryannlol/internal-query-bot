from app.config import settings

def chunk_text(text: str):
    chunks = []
    start = 0

    while start < len(text):
        end = start + settings.chunk_size
        chunk = text[start:end].strip()

        if len(chunk) >= settings.min_chunk_length:
            chunks.append(chunk)

        start = end - settings.chunk_overlap

    return chunks

def create_chunks(docs):
    all_chunks = []
    for doc in docs:
        # Change "document_content" to "text" to match the loader
        for chunk in chunk_text(doc["text"]): 
            all_chunks.append({
                "text": chunk,
                "source": doc["source"]
            })
    print('after loop ',all_chunks)
    return all_chunks