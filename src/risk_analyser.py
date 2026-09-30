import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from src.schemas import DocumentRiskReport

load_dotenv()

# High-risk legal / contractual query anchors
RISK_QUERY_TOPICS = [
    "liability limits, indemnification, direct or indirect damages",
    "termination for cause or convenience, lock-in, notice periods",
    "confidentiality duration, intellectual property ownership, data transfer",
    "penalties, payment defaults, late fees, operational limits and pricing"
]

def gather_risk_context(vector_db, top_k_per_topic: int = 2) -> str:
    """
    Vector store se multiple risk-focused queries chala kar relevant context gather karta hai.
    """
    unique_passages = set()
    
    for topic in RISK_QUERY_TOPICS:
        docs = vector_db.similarity_search(topic, k=top_k_per_topic)
        for doc in docs:
            page_no = doc.metadata.get("page", "Unknown")
            # Passage ko context set me add karte hain with citation
            unique_passages.add(f"[Source Page {page_no}]: {doc.page_content.strip()}")
            
    return "\n\n---\n\n".join(unique_passages)


def analyze_document_risks(vector_db, document_name: str) -> DocumentRiskReport:
    """
    Context ko LLM me bhej kar structured DocumentRiskReport generate karta hai.
    """
    # 1. Relevant risk context retrieve karo
    retrieved_context = gather_risk_context(vector_db)
    
    # 2. LLM setup aur Pydantic schema binding
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        temperature=0.0
    )
    structured_llm = llm.with_structured_output(DocumentRiskReport)
    
    # 3. Targeted Prompt
    prompt = f"""
You are a senior enterprise contract and document risk auditor.
Analyze the following retrieved document excerpts and extract significant operational, financial, and legal risks.

Document Name: {document_name}

Retrieved Excerpts:
{retrieved_context}

Audit Instructions:
1. Identify any potential risk in the text.
2. For each identified risk, populate:
   - category (from the defined categories)
   - level (LOW, MEDIUM, HIGH, CRITICAL)
   - clause_title
   - issue_description
   - verbatim_evidence (Quote EXACT text from the excerpts; do not alter or summarize this quote)
   - recommended_mitigation
3. If a risk category does not have any hazardous clause in the provided text, do NOT make up or hallucinate one.
4. Provide a clear 2-3 sentence overall summary and an overall risk score.
"""

    report = structured_llm.invoke(prompt)
    return report


if __name__ == "__main__":
    from src.parser import load_and_chunk_pdf
    from src.vectorstore import get_vector_store
    
    pdf_path = r"src\CognoDB-Assignment-2-Application.docx (1).pdf"
    
    print("1. Parsing document...")
    chunks = load_and_chunk_pdf(pdf_path)
    
    print("2. Loading into Vector Store...")
    v_db = get_vector_store(chunks)
    
    print("3. Analyzing risks with Gemini...")
    report: DocumentRiskReport = analyze_document_risks(v_db, document_name="CognoDB_Assignment.pdf")
    
    print("\n================ RISK REPORT ================")
    print(report.model_dump_json(indent=2))