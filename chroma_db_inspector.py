"""
Notes - 
1. In a chromadb persistent direcotry , the data is stored in a folder structure where each collection has its own folder. Inside each collection folder, there are files that store the embeddings, metadata, and documents. The structure is designed to allow for efficient storage and retrieval of data.

2.The core metadata lives in SQLIte , the vectors live in Parquet Segment . 
"""

#the purpose of this script is to inspect the contents of the chromadb vector store and understand how the data is stored and organized. It will help us to debug and troubleshoot any issues related to the vector store and also to understand the structure of the data for better querying and retrieval.

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


   
   

        
if __name__ == "__main__":
    show_collections_data()
    
'''
collections = client.list_collections()
for collection in collections:
    print(f"Collection Name: {collection.name}")
    print(f"Collection Peek : {collection.peek}")
'''