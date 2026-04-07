import os

docs_path = "data"  # Directory where the .txt documents are stored
chunk_size = 150    # Number of words per chunk
overlap = 25    # Number of overlapping words between chunks


def load_documents(path = docs_path):
    """
    Load all .txt documents from the specified directory and return a list of dictionaries with filename and content.
    """
    
    docs = []
    for fname in os.listdir(path):
        if fname.endswith(".txt"):
            with open(os.path.join(path, fname), "r", encoding="utf-8") as f:
                content = f.read().strip()
                docs.append({"filename": fname, "content": content})
                
    return docs

def chunk_text(text, chunk_size = chunk_size, overlap = overlap):
    """
    Split text into chunks of 'chunk_size' words, with overlapping text based on the 'overlap' parameter.
    """
    words = text.split()
    chunks = []

    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

def ingest_documents():
    """
    Load documents, chunk them, and return a list of chunks with metadata.
    """
    docs = load_documents()
    all_chunks = []

    for doc in docs:
        chunks = chunk_text(doc["content"])
        
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "content": chunk,
                "filename": doc["filename"],
                "chunk_index": i
            })

    return all_chunks

def vectorize_chunks(chunks):
    """
    Placeholder function for vectorizing chunks. In a real implementation, this would convert text chunks into vector representations.
    """
    # This is where you would integrate your vectorization logic (LLM, vector database", etc.)
    pass
    
# Uncomment for debugging purposes to see the ingested chunks
#for i, chunk in enumerate(chunks[:]):
#    print(f"--- Chunk {i+1} ---")
#    print(f"Filename: {chunk['filename']}")
#    print(f"Chunk index: {chunk['chunk_index']}")
#    print(f"Content preview: {chunk['content']}...")
#    print()