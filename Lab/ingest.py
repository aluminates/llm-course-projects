from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from traceback import print_exc
import os

DATA_PATH = "C:/Users/Ria/OneDrive/Desktop/PESU/UE21CS326C - Large Language Models/Day 3/Lab/datasets"
DB_CHROMA_PATH = "C:/Users/Ria/OneDrive/Desktop/PESU/UE21CS326C - Large Language Models/Day 3/Lab/chromaDB"
from sentence_transformers import SentenceTransformer
EMBEDDINGS_MODEL = SentenceTransformer("thenlper/gte-large")

def get_docs():
    """
    Loads the documents from the given source where each doc has page_content and metadata.
    Now includes additional metadata.
    """
    loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader, recursive=True)
    docs = loader.load()
    
    # Add additional metadata
    for doc in docs:
        file_path = doc.metadata['source']
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        doc.metadata.update({
            'file_name': file_name,
            'file_size': file_size,
            'document_type': 'PDF'
        })
    
    return docs

def get_chunks(docs, chunk_size=200, chunk_overlap=25):
    """
    Given docs obtained by using LangChain loader, split these to chunks and return them
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    texts = text_splitter.split_documents(docs)
    
    # Ensure metadata is preserved in chunks
    for i, text in enumerate(texts):
        text.metadata['chunk_id'] = i
    
    return texts

def get_embeddings_model(model_name="thenlper/gte-large"):
    if model_name is None:
        model_name = EMBEDDINGS_MODEL
    embeddings_model = HuggingFaceEmbeddings(model_name=model_name)
    return embeddings_model

def create_vector_store(texts, embeddings, db_path, use_db="chroma"):
    """
    Given the chunks, their embeddings and path to save the db, save and persist the data in the data store
    """
    flag = True
    try:
        if use_db == "chroma":
            db = Chroma.from_documents(texts, embeddings, persist_directory=db_path)
        else:
            print("Unknown db type, exiting!")
            db = None
            import sys
            sys.exit(-1)
        db.persist()
    except:
        flag = False
        print_exc()
        print("Exception when creating data store: ", db_path, use_db)
    return flag

def ingest():
    """
    Ingest PDF files from the given data source.
    """
    # 1. Load the data from the data source
    docs = get_docs()
    
    # 2. Chunk the documents
    texts = get_chunks(docs)
    print(len(docs), len(texts))
    
    # 3. get the embedding model
    embs_model = get_embeddings_model()
    
    # 4. Use the embedding model to vectorize and save it in db
    flag = create_vector_store(texts, embs_model, DB_CHROMA_PATH, use_db="chroma")
    if flag:
        print("Vectorstore created!")

if __name__ == '__main__':
    ingest()