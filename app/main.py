from fastapi import FastAPI
from app.api import router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import APIRouter


app = FastAPI(
    title="Internal Query Bot",
    description="Internal knowledge retrieval system using RAG"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
@app.get("/list-docs")
async def list_docs():
    files = os.listdir("data/documents")
    # Only return markdown files
    md_files = [f for f in files if f.endswith('.md')]
    return {"files": md_files}

@app.get("/get-doc/{filename}")
async def get_doc(filename: str):
    file_path = os.path.join("data/documents", filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return {"content": f.read()}
    return {"error": "File not found"}

app.include_router(router)

