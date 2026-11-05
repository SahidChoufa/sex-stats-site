
"""
retrieve.py

Purpose:
Search the local German legal database
for passages relevant to a user's question.
"""

import os

import chromadb
import ollama

from dotenv import load_dotenv


load_dotenv()

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="german_laws"
)


def retrieve_legal_documents(question, number_of_results=5):
    """
    Retrieve the most relevant legal passages.

    1. Embed the user's question.
    2. Search ChromaDB.
    3. Return the original text and metadata.
    """

    response = ollama.embed(
        model=EMBEDDING_MODEL,
        input=question
    )

    question_embedding = response["embeddings"][0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=number_of_results
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    retrieved_passages = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        retrieved_passages.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "distance": distance
        })

    return retrieved_passages


if __name__ == "__main__":

    question = input("Your legal question: ")

    results = retrieve_legal_documents(question)

    for result in results:

        print("\n-------------------------")
        print("Source:", result["source"])
        print("Page:", result["page"])
        print("Distance:", result["distance"])
        print("\n", result["text"])
