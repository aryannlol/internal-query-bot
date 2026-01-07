# app/retrieval/test_retrieval.py
from app.retrieval.retriever import Retriever

if __name__ == "__main__":
    r = Retriever()

    while True:
        q = input("\nQuery: ")
        if q.lower() in ["exit", "quit"]:
            break

        results = r.retrieve(q)

        if not results:
            print("No relevant information found.")
            continue

        for i, res in enumerate(results, 1):
            print(f"\nResult {i}")
            print("Source:", res["source"])
            print("Score:", res["score"])
            print("Content:", res["content"][:300], "...")
