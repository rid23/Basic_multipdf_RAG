"""
Notes - 
1. In a chromadb persistent direcotry , the data is stored in a folder structure where each collection has its own folder. Inside each collection folder, there are files that store the embeddings, metadata, and documents. The structure is designed to allow for efficient storage and retrieval of data.

2.The core metadata lives in SQLIte , the vectors live in Parquet Segment . 
"""

import chromadb
from chromadb.config import Settings

client = chromadb.Client(
    Settings(persist_directory="./vector_store")
)
'''
collection = client.get_collection(name="hacking_pdfs")
print(f"Collection Name: {collection.name}")
print(f"Collection Peek : {collection.peek}")

'''
collections = client.list_collections()
for collection in collections:
    print(f"Collection Name: {collection.name}")
    print(f"Collection Peek : {collection.peek}")