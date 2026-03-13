import chromadb
from rich import print
import os

#the purpose of this script is to query the vector store and retrieve relevant documents based on user queries. It will handle the interaction with the ChromaDB collection and return the results to the user.

class query_client:

    """this is class is responsible for querying the vector store and retrieving relevant documents based on user queries. It will handle the interaction with the ChromaDB collection and return the results to the user."""

    def __init__(self , collection_name: str = "hacking_pdfs" , persistent_directory: str = "./vector_store"):
        self.collections_name = collection_name
        self.persistent_directory = persistent_directory
        self.Client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):
        '''Initialize the chromadb vector store and create a collection'''
        try:
            #os.makedirs(self.persistent_directory , exist_ok=True)
            self.Client = chromadb.PersistentClient(path=self.persistent_directory)

            #get collection
            self.collection = self.Client.get_collection(
                name=self.collections_name , 
                
            )
            print(f'Vector store initialized : Collection -> {self.collections_name}')
            print(f'Existing documents in collection {self.collection.count()}')
        except Exception as e:
            print(f'There was an error initializing the vector store {e}')
            raise
    def query_collection(self , query: str , n_results: int = 5):
        '''Query the collection and return relevant documents'''
        try:
            result_docs = self.collection.query(
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
            '''
            for i in range(len(unique_documents)):
                print(f"Result {i+1}:")
                print(f"Document: {unique_documents[i][0]}")
                print(f"Source: {unique_documents[i][1]['title']}")
                print("-" * 20)
                '''
            return unique_documents
        except Exception as e:
            print(f'There was an error querying the collection {e}')
            raise
if __name__ == "__main__":    
    query_client_instance = query_client()
    user_query = input("Enter your query: ")
    query_client_instance.query_collection(query=user_query , n_results=5)