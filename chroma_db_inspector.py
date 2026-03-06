"""
Notes - 
1. In a chromadb persistent direcotry , the data is stored in a folder structure where each collection has its own folder. Inside each collection folder, there are files that store the embeddings, metadata, and documents. The structure is designed to allow for efficient storage and retrieval of data.

2.The core metadata lives in SQLIte , the vectors live in Parquet Segment . 
"""

import chromadb
from chromadb.config import Settings
from rich import print
import os
client = chromadb.PersistentClient(path='./vector_store')
collection = client.get_collection(name="hacking_pdfs")
print(f"Collection Name: {collection.name}")
#print(f"Collection Peek : {collection.peek()}")

def show_collections_data():
    data = collection.get(include=["documents" , "metadatas" , "embeddings"])
    print(f"Number of documents in collection: {len(data['documents'])}")
    print(f"Documents : {data['documents'][:2]}")   
    print(f"Metadatas : {data['metadatas'][:2]}")
    print(f"Embeddings : {data['embeddings'][:2]}")
    print(f"id : {data['ids'][:2]}")


def query_collection(n_results: int = 5):
    query = input("Enter your query: ")
    result_docs = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents" , "metadatas" , "embeddings"]
    )
    documents = result_docs['documents'][0]
    metadatas = result_docs['metadatas'][0]
    print(f"Query : {query}")
    print(f"Number of results: {len(result_docs['documents'][0])}")

    #deduplicate while preserving order 
    seen = set()
    unique_documents = []
    for doc , meta in zip(documents , metadatas):
        if doc not in seen:
            seen.add(doc)
            unique_documents.append((doc , meta))
    print(f"Number of unique results: {len(unique_documents)}")
    for i in range(len(unique_documents)):
        print(f"Result {i+1}:")
        print(f"Document: {unique_documents[i][0]}")
        print(f"Source: {unique_documents[i][1]['title']}")
        print("-" * 20)
   
   

        
if __name__ == "__main__":
    #show_collections_data()
    query_collection()
'''
collections = client.list_collections()
for collection in collections:
    print(f"Collection Name: {collection.name}")
    print(f"Collection Peek : {collection.peek}")
'''