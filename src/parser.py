from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_chunk_pdf(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " "]
    )
    result = splitter.split_documents(docs)
    return result

if __name__ == "__main__":
    pdf_path = r"src\CognoDB-Assignment-2-Application.docx (1).pdf"
    chunks = load_and_chunk_pdf(pdf_path)
    print(f"Total chunks: {len(chunks)}")