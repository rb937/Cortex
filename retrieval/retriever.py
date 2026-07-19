import chromadb
import ollama
from pathlib import Path

def get_embedding(text: str) -> list[float]:
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]

def retrieve_chunks(query: str, db_path: str, top_k: int = 4):
    """Retrieve the top_k most relevant chunks for a query."""
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection("coursework")

    query_embedding = get_embedding(query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = results["documents"][0]
    sources = [meta["source"] for meta in results["metadatas"][0]]
    return list(zip(chunks, sources))

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    db_path = str(project_root / "chroma_db")

    query = "What is logistic regression?"
    results = retrieve_chunks(query, db_path)

    for i, (chunk, source) in enumerate(results):
        print(f"\n--- Result {i+1} (from {source}) ---")
        print(chunk[:300])