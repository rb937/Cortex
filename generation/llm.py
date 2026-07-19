import ollama
from backends import generate

def generate_answer(query: str, retrieved_chunks: list[tuple[str, str]], backend: str = "ollama") -> str:
    """Build a prompt from retrieved chunks and generate an answer."""
    context = "\n\n".join([f"[Source: {source}]\n{chunk}" for chunk, source in retrieved_chunks])

    prompt = f"""You are a helpful study assistant. Answer the question using ONLY the context below.
If the context doesn't contain the answer, say so honestly instead of making something up.

Context:
{context}

Question: {query}

Answer:"""
    return generate(prompt, backend=backend)

if __name__ == "__main__":
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent / "retrieval"))
    from retriever import retrieve_chunks

    project_root = Path(__file__).resolve().parent.parent
    db_path = str(project_root / "chroma_db")

    print("Ask your questions based on the documents stored in the vector database. Type 'exit' or 'quit' to quit.")
    while True:
        query = input("Question: ")
        if query.lower() in ["exit", "quit"]:
            break

        chunks = retrieve_chunks(query, db_path)
        answer = generate_answer(query, chunks)
        print(f"\nAnswer: {answer}\n")