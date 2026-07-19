import chromadb
import ollama
from pathlib import Path

def get_embedding(text: str) -> list[float]:
    response = ollama.embeddings(model="nomic-embed-text", prompt=text)
    return response["embedding"]

def build_vector_store(chunks: list[tuple[str, str]], db_path: str = "./chroma_db"):
    """
    chunks: list of (filename, chunk_text) tuples
    Embeds each chunk and stores it in a persistent Chroma collection.
    """
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection("coursework")

    for i, (filename, chunk) in enumerate(chunks):
        embedding = get_embedding(chunk)
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"source": filename}]
        )
        print(f"Stored chunk {i+1}/{len(chunks)} from {filename}")

    return collection

if __name__ == "__main__":
    import sys
    sys.path.append(str(Path(__file__).resolve().parent.parent / "ingestion"))
    from loader import load_all_documents
    from chunker import chunk_text

    project_root = Path(__file__).resolve().parent.parent
    docs_path = project_root / "data" / "raw_docs"

    docs = load_all_documents(str(docs_path))
    all_chunks = []
    for filename, text in docs.items():
        chunks = chunk_text(text)
        all_chunks.extend([(filename, c) for c in chunks])

    print(f"Total chunks to embed: {len(all_chunks)}")
    build_vector_store(all_chunks, db_path=str(project_root / "chroma_db"))
    print("Done. Vector store built.")