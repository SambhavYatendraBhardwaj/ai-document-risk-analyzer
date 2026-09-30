# 🛡️ AI Document Risk Analyzer

A production-grade Retrieval-Augmented Generation (RAG) system engineered to audit contractual, legal, and operational documents. The system systematically extracts categorized contractual hazards (Liability, IP Ownership, Penalties, Compliance) into strictly validated schemas and runs an automated Groundedness verification layer to eliminate LLM hallucinations.

---

## 🚀 Key Features

- **Chunking & Ingestion Engine:** Parses digital PDFs using PyMuPDF and splits unstructured legal text with recursive character splitting to preserve contextual semantic boundaries.
- **Local Vector Indexing:** Indexes embedded chunks using ChromaDB and Google Generative AI embeddings for targeted similarity retrieval across legal risk query anchors.
- **Strictly Typed Structured Extraction:** Utilizes Google Gemini Flash coupled with Pydantic v2 schemas (`DocumentRiskReport`) to enforce consistent typing, risk categorization, severity ratings, and actionable mitigations.
- **Automated Groundedness & Evaluation Pipeline:** Implements a post-generation verification engine that evaluates extracted verbatim evidence against raw document context via normalized substring matching to eliminate model fabrications.
- **Dual Presentation Layer:** 
  - **FastAPI Backend:** Production-grade REST API supporting multipart file uploads, Swagger UI (`/docs`), and automatic cleanup routines for temporary files.
  - **Streamlit Dashboard:** Visual UI featuring KPI metrics, dynamic risk severity badges, and interactive collapsible risk cards.

---

## 🏗️ Architecture & Pipeline Flow

```text
User PDF
   │
   ▼
[ PyMuPDF Document Loader ] ──► [ Recursive Character Text Splitter ]
                                           │
                                           ▼
                                [ Google GenAI Embeddings ]
                                           │
                                           ▼
                                  [ ChromaDB Store ]
                                           │
                                           ▼
                             [ Targeted Legal Anchors Retrieval ]
                                           │
                                           ▼
                             [ Gemini Flash + Pydantic v2 ]
                                           │
                                           ▼
                           [ Groundedness Verification Check ]
                                           │
                  ┌────────────────────────┴────────────────────────┐ 
[ FastAPI REST Endpoint ]                           [ Streamlit Frontend ]
Tech Stack
LLM & Reasoning: Google Gemini Flash (ChatGoogleGenerativeAI)

Orchestration & RAG: LangChain, ChromaDB

Validation: Pydantic v2

Backend API: FastAPI, Uvicorn, Python-Multipart

Frontend UI: Streamlit, Requests

Document Processing: PyMuPDF, LangChain Community

📂 Project Structure
Plaintext
├── src/
│   ├── parser.py          # PDF ingestion and chunking logic
│   ├── schemas.py         # Pydantic v2 models for structured risk outputs
│   ├── vectorstore.py     # ChromaDB embedding & retrieval setup
│   ├── risk_analyser.py   # Gemini reasoning & structured extraction
│   ├── evaluator.py       # Groundedness & Precision/Recall evaluation pipeline
│   ├── app.py             # FastAPI backend server
│   └── frontend.py        # Streamlit user interface
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (API keys)
├── .gitignore             # Excluded files and folders
└── README.md              # Project documentation
⚙️ Installation & Setup
Clone the repository:

Bash
git clone [https://github.com/SambhavYatendraBhardwaj/ai-document-risk-analyzer.git](https://github.com/SambhavYatendraBhardwaj/ai-document-risk-analyzer.git)
cd ai-document-risk-analyzer
Create and activate a virtual environment:

Bash
python -m venv myenv
# Windows (PowerShell):
.\myenv\Scripts\Activate.ps1
# Linux / macOS:
source myenv/bin/activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure environment variables:
Create a .env file in the root directory:

Code snippet
GOOGLE_API_KEY=your_gemini_api_key_here
🖥️ Running the Application
1. Launch FastAPI Backend
Bash
python -m uvicorn src.app:app --reload
Interactive Swagger documentation will be accessible at: http://127.0.0.1:8000/docs

2. Launch Streamlit Frontend
In a separate terminal (with virtual environment activated):

Bash
streamlit run src/frontend.py
Streamlit web dashboard will open at: http://localhost:8501


---

1. Apne GitHub repository page par jao[cite: 5].
2. Wahan **"Add a README"** green button par click karo[cite: 5].
3. Upar ka pura code paste karo aur neeche **"Commit changes"** par click kar do.

<FollowUp label="Kya README add ho gayi aur ab resume ke points banayein?" query="README


────────────────────────┐
                  ▼                                                 ▼
      [ FastAPI REST Endpoint ]                           [ Streamlit Frontend ]
