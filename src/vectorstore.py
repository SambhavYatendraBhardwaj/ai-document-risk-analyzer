import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
load_dotenv()
def get_vector_store(chunks, persist_directory: str = "chroma_db"):
    """
     WILL embed chunksa nd will store them in chroma db.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    return vector_db

def search_similar_chunks(vector_db, query: str, top_k: int = 3):
    """
    Query ke basis par sabse relevant chunks search karke return karta hai.
    """
    results = vector_db.similarity_search(query, k=top_k)
    return results

if __name__ == "__main__":
    from src.parser import load_and_chunk_pdf
    
    # 1. Chunks load karo
    pdf_path = r"src\CognoDB-Assignment-2-Application.docx (1).pdf"
    chunks = load_and_chunk_pdf(pdf_path)
    
    # 2. Vector DB create karo
    print("Creating vector store...")
    vector_db = get_vector_store(chunks)
    
    # 3. Test Query chala kar check karo
    query = "free tier limits and instance size"
    print(f"\nSearching for: '{query}'")
    matched_docs = search_similar_chunks(vector_db, query, top_k=2)
    
    for i, doc in enumerate(matched_docs):
        print(f"\n--- Match {i+1} (Page {doc.metadata.get('page')}) ---")
        print(doc.page_content[:200])