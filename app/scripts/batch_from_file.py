from pathlib import Path
import json
from app.retrieval.retriever import Retriever
from app.generation.answer_generator import AnswerGenerator

BASE_DIR = Path(__file__).parent
QUESTIONS_FILE = BASE_DIR / "questions.txt"
OUTPUT_FILE = BASE_DIR / "results.json"

def run_batch():
    retriever = Retriever()
    generator = AnswerGenerator()

    with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
        questions = [q.strip() for q in f.readlines() if q.strip()]

    results = []

    for i, question in enumerate(questions, 1):
        print("\n" + "=" * 80)
        print(f"Q{i}: {question}")

        chunks = retriever.retrieve(question)

        entry = {
            "question": question,
            "answer": None,
            "sources": [],
            "confidence": "Low",
            "retrieved_chunks": []
        }

        if not chunks:
            print("Answer: I do not have enough information to answer this.")
            results.append(entry)
            continue

        # store retrieval info
        for c in chunks:
            entry["retrieved_chunks"].append({
                "source": c["source"],
                "score": c["score"],
                "content": c["content"]
            })

        try:
            result = generator.generate(question, chunks)
        except Exception as e:
            print("LLM failed:", e)
            results.append(entry)
            continue

        entry["answer"] = result["answer"]
        entry["sources"] = result["sources"]
        entry["confidence"] = result["confidence"]

        print("\nAnswer:")
        print(entry["answer"])
        print("\nSources:", entry["sources"])
        print("Confidence:", entry["confidence"])

        results.append(entry)

    # save JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"Batch completed. Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_batch()