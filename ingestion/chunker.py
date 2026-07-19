def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks by word count.
    chunk_size: target words per chunk
    overlap: words shared between consecutive chunks (preserves context across boundaries)
    """
    words = text.split()
    chunks = []
    
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    
    return chunks

if __name__ == "__main__":
    from loader import load_all_documents
    
    docs = load_all_documents("./data/raw_docs")
    print(f"Loaded {len(docs)} documents")
    
    all_chunks = []
    for filename, text in docs.items():
        chunks = chunk_text(text)
        print(f"{filename}: {len(chunks)} chunks")
        all_chunks.extend([(filename, c) for c in chunks])
    
    print(f"\n--- Sample chunk from {all_chunks[0][0]} ---")
    print(all_chunks[0][1][:300])