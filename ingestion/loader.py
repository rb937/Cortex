from markitdown import MarkItDown
from pathlib import Path

def load_document(file_path: str) -> str:
    md = MarkItDown()
    result = md.convert(file_path)
    return result.text_content

def load_all_documents(folder_path: str) -> dict:
    md = MarkItDown()
    documents = {}
    folder = Path(folder_path)
    
    for file in folder.glob("*"):
        if file.suffix.lower() in [".pdf", ".docx", ".pptx"]:
            print(f"Loading: {file.name}")
            result = md.convert(str(file))
            documents[file.name] = result.text_content
    
    return documents

if __name__ == "__main__":
    docs = load_all_documents("data/raw_docs")
    
    for filename, text in docs.items():
        print(f"\n{'='*50}")
        print(f"FILE: {filename}")
        print(f"{'='*50}")
        print(text[:1000])
        print(f"\n... (total length: {len(text)} chars)")