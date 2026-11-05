
"""
ingest.py

Purpose:
1. Read German legal PDF documents.
2. Extract their text page by page.
3. Split text into smaller chunks.
4. Generate embeddings using Ollama.
5. Store the chunks in ChromaDB.

Each chunk keeps its source filename and PDF page number.
"""

import os
import hashlib
from pathlib import Path

import chromadb
import ollama

from dotenv import load_dotenv
from pypdf import PdfReader


# --------------------------------------------------
# 1. Load configuration
# --------------------------------------------------

load_dotenv()

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)

DOCUMENT_FOLDER = Path("documents/laws")

DB_FOLDER = "./chroma_db"

COLLECTION_NAME = "german_laws"


# --------------------------------------------------
# 2. Initialize the vector database
# --------------------------------------------------

client = chromadb.PersistentClient(path=DB_FOLDER)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    metadata={"hnsw:space": "cosine"}
)


# --------------------------------------------------
# 3. Split text into chunks
# --------------------------------------------------

def split_text(text, chunk_size=1200, overlap=200):
    """
    Split text into overlapping chunks.

    chunk_size: maximum approximate number of characters.
    overlap: number of characters repeated between chunks.

    Overlap helps preserve legal context when a provision
    crosses a chunk boundary.
    """

    words = text.split()

    chunks = []
    current_chunk = []

    current_length = 0

    for word in words:

        current_chunk.append(word)
        current_length += len(word) + 1

        if current_length >= chunk_size:

            chunks.append(" ".join(current_chunk))

            # Keep some previous words for context.
            overlap_words = []

            overlap_length = 0

            for previous_word in reversed(current_chunk):

                overlap_words.insert(0, previous_word)
                overlap_length += len(previous_word) + 1

                if overlap_length >= overlap:
                    break

            current_chunk = overlap_words
            current_length = overlap_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


# --------------------------------------------------
# 4. Generate embeddings with Ollama
# --------------------------------------------------

def generate_embeddings(texts):
    """
    Convert a list of text passages into vectors.

    Ollama runs locally, so the text is sent to your
    local Ollama server.
    """

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=texts
    )

    return response["embeddings"]


# --------------------------------------------------
# 5. Process a PDF document
# --------------------------------------------------

def process_pdf(pdf_path):

    print(f"\nProcessing: {pdf_path.name}")

    reader = PdfReader(str(pdf_path))

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if not text or not text.strip():
            print(f"Skipping empty page: {page_number}")
            continue

        chunks = split_text(text)

        if not chunks:
            continue

        # Generate vectors in batches.
        batch_size = 32

        for start in range(0, len(chunks), batch_size):

            batch = chunks[start:start + batch_size]

            embeddings = generate_embeddings(batch)

            ids = []
            metadatas = []

            for index, chunk in enumerate(batch):

                chunk_number = start + index

                unique_id = hashlib.sha256(
                    f"{pdf_path.name}:{page_number}:{chunk_number}".encode()
                ).hexdigest()

                ids.append(unique_id)

                metadatas.append({
                    "source": pdf_path.name,
                    "page": page_number,
                    "chunk": chunk_number,
                })

            # Upsert avoids creating duplicate records
            # when the same PDF is indexed again.
            collection.upsert(
                ids=ids,
                documents=batch,
                embeddings=embeddings,
                metadatas=metadatas
            )

    print(f"Finished: {pdf_path.name}")


# --------------------------------------------------
# 6. Process every PDF in the folder
# --------------------------------------------------

def ingest_documents():

    pdf_files = list(DOCUMENT_FOLDER.glob("*.pdf"))

    if not pdf_files:
        print("No PDF documents found!")
        return

    for pdf_path in pdf_files:
        process_pdf(pdf_path)

    print("\nAll legal documents indexed successfully.")


if __name__ == "__main__":
    ingest_documents()
