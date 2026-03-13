import os
from rich import print
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#imports for embedding models and vector stores will go here
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import chromadb
from chromadb.config import Settings
import uuid
from typing import List, Dict, Any , Tuple
from langchain_chroma import Chroma
import hashlib

#importing the query client to query the vector store and retrieve relevant documents based on user queries.
from rag_query import query_client

#importing the llm cient 
from llm_brain import the_brain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

def load_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    print(f"loading pdfs from {file_path}")
    pdfs = os.listdir(file_path)
    all_documents = []
    for file in pdfs:
        if file.endswith('.pdf'):
            loader = PyMuPDFLoader(os.path.join(file_path, file))
            documents = loader.load()
            print(f"Loaded {len(documents)} documents from {file}")
            all_documents.extend(documents)

    print(f"Total documents loaded: {len(all_documents)}")
    return all_documents


def text_splitter(documents , chunk_size=1000, chunk_overlap=200):
    """Splitting documents into chunks of text."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""],
        length_function=len)
    chunks = text_splitter.split_documents(documents)
    print(f'''First chunk: {chunks[0].page_content[:500]}''')
    print(f'{len(documents)} documents were split into {len(chunks)} chunks.')
    return chunks


class EmbeddingManager:
    """Class to manage embedding models and vector stores. This class will handle the creation of embeddings and the management of vector stores."""
    def __init__(self , model_name = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.embeddings = None
        self._load_model()

    def _load_model(self):
        """Load the embedding model."""
        try:
            print(f"Loading embedding model: {self.model_name}")
            self.embeddings = SentenceTransformer(self.model_name)
            print(f'Embedding model "{self.model_name}" loaded successfully. Model details: {self.embeddings} , model type: {type(self.embeddings)} , model dimension: {self.embeddings.get_sentence_embedding_dimension()}')
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def generate_embeddings(self , texts: List[str]) -> np.ndarray:
        """Generate embeddings for a list of texts"""
        if not self.embeddings:
            raise ValueError("Model Not Loaded :-> ")
        print(f'Generate Embeddings for {len(texts)} texts')
        embeddings = self.embeddings.encode(texts , show_progress_bar=True)
        print(f'Generated embeddings with shape : {embeddings.shape}')
        return embeddings
    



class VectorStore:
    #initializing all the essential variables necessary for the vector store .
    def __init__(self , collection_name: str = "hacking_pdfs" , persistent_directory: str = "./vector_store"):
        self.collections_name = collection_name
        self.persistent_directory = persistent_directory
        self.Client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):
        '''Initialize the chromadb vector store and create a collection'''
        try:
            os.makedirs(self.persistent_directory , exist_ok=True)
            self.Client = chromadb.PersistentClient(path=self.persistent_directory)

            #get or create collection
            self.collection = self.Client.get_or_create_collection(
                name=self.collections_name , 
                metadata={"description":"Hacking knowledge collection"}
            )
            print(f'Vector store initialized : Collection -> {self.collections_name}')
            print(f'Existing documents in collection {self.collection.count()}')
        except Exception as e:
            print(f'There was an error initializing the vector store {e}')
            raise
    def show_collections(self):
        '''Show all collections in the vector store'''
        try:
            collections = self.Client.list_collections()
            print(f'Collections in the vector store: {[collection.name for collection in collections]}')
        except Exception as e:
            print(f'There was an error fetching collections from the vector store {e}')
            raise
    def delete_collection(self):
        '''Delete the collection from the vector store'''
        try:
            confirmation = input(f"Are you sure you want to delete the collection {self.collections_name}? This action cannot be undone. (yes/no): ")
            if confirmation.lower() == "yes":
                self.Client.delete_collection(name=self.collections_name)
                print(f'Collection {self.collections_name} deleted successfully.')
            else:
                print(f'Collection {self.collections_name} was not deleted.')
        except Exception as e:
            print(f'There was an error deleting the collection {self.collections_name} from the vector store {e}')
            raise
    def add_documents(self , documents: List[any] , embeddings: np.ndarray):
        """
        Add Documents and embeddings to the vector store . 
        This function will take in a list of documents and their corresponding embeddings and add them to the vector store.
        """
        if len(documents) != len(embeddings):
            raise ValueError("The number of documents and embeddings must be the same.")
        print(f"adding {len(documents)}")

        #preparing data for chromaDB
        ids = []
        metadatas = []
        documents_text = []
        embeddings_list = []

        for i , (doc , embedding) in enumerate(zip(documents , embeddings)):
            #generate unique ids
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)

            #prepare metadata
            metadata = dict(doc.metadata)
            metadata['doc_index'] = i
            metadata['content_length'] = len(doc.page_content)
            metadatas.append(metadata)

            #adding document content
            documents_text.append(doc.page_content)

            #adding the embeddings
            embeddings_list.append(embedding)

        #adding the ids , documents , embeddings to the collection
        try:
            self.collection.add(
                ids = ids,
                embeddings = embeddings_list,
                metadatas = metadatas,
                documents = documents_text
            )
        except Exception as e:
            print(f'ERROR adding documents to the vector store {e}')
            raise
        print(f'Vector Store Populataion complete.')


def intialize_vector_store_add_documents():
    '''Function to initialize the vector store and add documents and their corresponding embeddings to the vector store.'''
    pdf_directory = "pdfs"  # Change this to your PDF directory
    all_documents = load_pdf(os.path.join(os.getcwd(), pdf_directory))
    all_documents_chunks = text_splitter(all_documents)

    #extracting chunks [Document] page_content text into a list
    all_documents_chunks_page_content = [chunk.page_content for chunk in all_documents_chunks]

    # initializing the embedding manager .
    embedding_manager = EmbeddingManager() 
    #turning the chunks page_content into embeddings
    all_documents_chunks_embeddings = embedding_manager.generate_embeddings(texts=all_documents_chunks_page_content)
    
    #initializing the vector store and adding the documents and their corresponding embeddings to the vector store.
    vector_store = VectorStore()
    vector_store.add_documents(documents=all_documents_chunks , embeddings=all_documents_chunks_embeddings)


def retrieve_context(query:str) -> str:
    """this function will take in a user query and retrieve relevant documents from the vector store based on the user query and return the merged context text to be used by the LLM brain to generate a response."""
    query_client_instance = query_client()
    docs_from_query = query_client_instance.query_collection(query=query , n_results=5)
    context_text_merged = " ".join([doc[0] for doc in docs_from_query])
    return context_text_merged


if __name__ == "__main__": 
    """initialize the vector store and add documents and their corresponding embeddings to the vector store. or query the vector store and retrieve relevant documents based on user input instructions."""
    action = input("Enter 'add' to add documents to the vector store or 'query' to query the vector store: ")
    if action.lower() == "add":
        intialize_vector_store_add_documents()
    elif action.lower() == "query":
        google_gemini_llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        
        
        while True:
            
            user_query = input("Enter your Query: ")
            if user_query == "quit":
                print("Exiting ................ ")
                break

            context_text_merged = retrieve_context(query=user_query)
            #print(f"Context - : {context_text_merged}") #printing the

            llm_result = the_brain(llm=google_gemini_llm , context=context_text_merged , query=user_query)
            print(llm_result)
    else:        
        print("Invalid action. Please enter 'add' or 'query'.")

    