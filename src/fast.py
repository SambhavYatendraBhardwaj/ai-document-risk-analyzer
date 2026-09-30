import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from src.parser import load_and_chunk_pdf
from src.vectorstore import get_vector_store
from src.risk_analyser import analyze_document_risks
from src.evaluator import calculate_groundedness_score

app = FastAPI(
    title="AI Document Risk Analyzer API",
    description="Production-ready Contract & Legal Document Risk Auditing with Groundedness Verification",
    version="1.0.0"
)

# Temporary directory for uploaded files
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def health_check():
    """Service health status check"""
    return {
        "status": "healthy",
        "service": "AI Document Risk Analyzer",
        "docs_url": "/docs"
    }


@app.post("/analyze-risk")
async def analyze_document(file: UploadFile = File(...)):
    """
    PDF upload karo aur structured risk assessment report prapt karo.
    """
    # 1. File validation
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # 2. Uploaded PDF ko temporarily save karo
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 3. Document parse aur chunk karo
        chunks = load_and_chunk_pdf(temp_path)
        if not chunks:
            raise HTTPException(
                status_code=400, 
                detail="Could not extract text. Ensure the PDF is not a scanned image."
            )

        raw_text = " ".join([c.page_content for c in chunks])

        # 4. ChromaDB vector store create karo (isolated collection per run)
        vector_db = get_vector_store(chunks)

        # 5. Gemini structured risk analysis execute karo
        report = analyze_document_risks(vector_db, document_name=file.filename)

        # 6. Groundedness hallucination verification calculate karo
        eval_metrics = calculate_groundedness_score(report, raw_text)

        # 7. Final response build karo
        return {
            "document_name": file.filename,
            "evaluation": eval_metrics,
            "risk_report": report.model_dump()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # Cleanup: temp file remove karo
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)