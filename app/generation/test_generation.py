from app.retrieval.retriever import Retriever
from app.generation.answer_generator import AnswerGenerator

if __name__ == "__main__":
    retriever = Retriever()
    generator = AnswerGenerator()

    while True:
        q = input("\nQuestion: ")
        if q.lower() in ["exit", "quit"]:
            break

        chunks = retriever.retrieve(q)
        result = generator.generate(q, chunks)

        print("\n--- ANSWER ---")
        print(result["answer"])
        print("\nSources:", result["sources"])
        print("Confidence:", result["confidence"])
    