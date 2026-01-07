from pathlib import Path

def load_documents(doc_dir: str):
    documents = []

    for path in Path(doc_dir).glob("*"):
        if path.suffix not in [".md", ".txt",".pdf"]:
            continue

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        documents.append({
            "text": text,
            "source": path.name
        })

    return documents