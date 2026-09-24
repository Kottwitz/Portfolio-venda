import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "./chroma_db"
DOCUMENTS_PATH = "./documentos"

def recarregar_base():
    # 1. Limpa o banco anterior se existir
    if os.path.exists(CHROMA_PATH):
        print("Removendo base de dados vetorial antiga...")
        shutil.rmtree(CHROMA_PATH)

    # 2. Carrega todos os arquivos da pasta documentos
    print(f"Lendo documentos de '{DOCUMENTS_PATH}'...")
    loader = DirectoryLoader(DOCUMENTS_PATH, glob="*.txt", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
    docs = loader.load()

    # 3. Divide em fragmentos
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)
    print(f"Total de {len(chunks)} fragmentos gerados.")

    # 4. Gera os embeddings e salva no ChromaDB
    print("Criando novos vetores no ChromaDB...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)
    print("✅ Base de conhecimento atualizada com sucesso!")

if __name__ == "__main__":
    recarregar_base()