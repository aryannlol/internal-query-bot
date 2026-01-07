from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """
    This is the Application configuration for Pydantic V1 (Compatible with ChromaDB 0.3.23),
    Further these Values can be overridden by environment variables or .env file.
    """
    # API Settings
    app_name: str = "Internal Query Bot"
    debug: bool = False

    # Paths
    documents_dir: Path = Path("data/documents")
    chroma_dir: Path = Path("index/chroma")

    # LLM Settings
    ollama_url: str = "http://localhost:11434/api/generate"
    ollama_model: str = "llama3"
    ollama_timeout: int = 120

    # Retrieval Settings
    top_k: int = 3
    distance_threshold: float = 1.6

    # Generation Settings
    max_chunks: int = 3
    max_chars_per_chunk: int = 1200

    # Chunking Settings
    chunk_size: int = 600
    chunk_overlap: int = 100
    min_chunk_length: int = 80

    # Embedding Settings
    embedding_model: str = "all-MiniLM-L6-v2"

    # Rate Limiting
    query_rate_limit: str = "10/minute"
    admin_upload_rate_limit: str = "50/hour"
    admin_rebuild_rate_limit: str = "3/hour"

    # ✅ In Pydantic V1, we use 'class Config' instead of 'model_config'
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# ✅ Global settings instance
settings = Settings()