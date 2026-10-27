 🛡️ AI Document Risk Analyzer

An end-to-end Retrieval-Augmented Generation (RAG) system that audits contractual, legal, and operational documents. It extracts categorized risks (Liability, IP Ownership, Penalties, Compliance) into strictly validated schemas, then runs a **groundedness check** that verifies each extracted piece of evidence actually exists in the source document, to catch hallucinated claims.

Why this project

LLMs can sound confident while inventing clauses that don't exist. In contract review that is unacceptable, so every risk the model reports is checked against the original text before it is shown.

 Key Features

- **Ingestion:** PyMuPDF loads digital PDFs; recursive character splitting preserves semantic boundaries.
- **Vector retrieval:** Chunks are embedded with Google Generative AI embeddings and stored in ChromaDB; targeted risk-category queries retrieve the relevant passages.
- **Structured extraction:** Gemini Flash + Pydantic v2 (`DocumentRiskReport`) enforce typed output: category, severity, evidence, and suggested mitigation.
- **Groundedness verification:** Extracted verbatim evidence is matched against the raw document text (normalized substring matching); unsupported claims are flagged.
- **Two interfaces:** FastAPI REST backend (multipart upload, Swagger UI at `/docs`) and a Streamlit dashboard (KPI metrics, severity badges, expandable risk cards).

 Results

> Fill these with your real numbers before publishing. Do not leave placeholders.

| Metric | Value |
|---|---|
| Documents tested | X |
| Risks extracted | X |
| Grounded (evidence verified in source) | X% |
| Precision / Recall (vs. manual labels) | X / X |

 Architecture

```
User PDF
   │
   ▼
[ PyMuPDF Loader ] ──► [ Recursive Text Splitter ]
                                │
                                ▼
                     [ Google GenAI Embeddings ]
                                │
                                ▼
                        [ ChromaDB Store ]
                                │
                                ▼
                  [ Targeted Risk-Query Retrieval ]
                                │
                                ▼
                    [ Gemini Flash + Pydantic v2 ]
                                │
                                ▼
                 [ Groundedness Verification Check ]
                                │
                 ┌──────────────┴──────────────┐
                 ▼                             ▼
      [ FastAPI REST Endpoint ]      [ Streamlit Frontend ]
```

 Tech Stack

| Layer | Tools |
|---|---|
| LLM | Google Gemini Flash (`ChatGoogleGenerativeAI`) |
| RAG / Orchestration | LangChain, ChromaDB |
| Validation | Pydantic v2 |
| Backend | FastAPI, Uvicorn, python-multipart |
| Frontend | Streamlit, Requests |
| Document processing | PyMuPDF, LangChain Community |

 Project Structure

```
├── src/
│   ├── parser.py          # PDF ingestion and chunking
│   ├── schemas.py         # Pydantic v2 models for structured risk output
│   ├── vectorstore.py     # ChromaDB embedding and retrieval
│   ├── risk_analyser.py   # Gemini reasoning and structured extraction
│   ├── evaluator.py       # Groundedness and precision/recall evaluation
│   ├── app.py             # FastAPI backend
│   └── frontend.py        # Streamlit UI
├── requirements.txt
├── .gitignore
└── README.md
```

Setup

```bash
git clone https://github.com/SambhavYatendraBhardwaj/ai-document-risk-analyzer.git
cd ai-document-risk-analyzer

python -m venv myenv
# Windows (PowerShell): .\myenv\Scripts\Activate.ps1
# Linux / macOS:        source myenv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root (never commit it):

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

 Run

**1. Start the API**

```bash
python -m uvicorn src.app:app --reload
```

Swagger docs: http://127.0.0.1:8000/docs

**2. Start the dashboard** (separate terminal, venv active)

```bash
streamlit run src/frontend.py
```

Dashboard: http://localhost:8501

 Limitations

- Supports digital (text-based) PDFs only; scanned documents need OCR.
- Groundedness uses substring matching, so paraphrased evidence may be flagged as unverified.
- Not legal advice; output should be reviewed by a human.

## Roadmap

- OCR support for scanned contracts
- Semantic (embedding-based) groundedness scoring
- Automated test suite and CI
