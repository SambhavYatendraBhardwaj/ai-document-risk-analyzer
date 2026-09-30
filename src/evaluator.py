from typing import List, Dict, Set
from src.schemas import DocumentRiskReport

def calculate_groundedness_score(report: DocumentRiskReport, raw_document_text: str) -> Dict[str, float]:
    """
    Check karta hai ki LLM ne jo quotes/evidence diye hain,
    kya wo actual raw document ke andar exist karte hain ya fabricate kiye gaye hain.
    """
    if not report.risks_detected:
        return {"groundedness_score": 1.0, "total_evidences": 0, "verified_evidences": 0}

    normalized_raw = " ".join(raw_document_text.split()).lower()
    verified_count = 0
    total = len(report.risks_detected)

    for item in report.risks_detected:
        clean_evidence = " ".join(item.verbatim_evidence.split()).lower()
        # Substring match ya short snippet check
        if clean_evidence in normalized_raw or len(clean_evidence) < 10:
            verified_count += 1

    score = verified_count / total if total > 0 else 1.0
    return {
        "groundedness_score": round(score, 3),
        "total_evidences": total,
        "verified_evidences": verified_count
    }


def calculate_risk_metrics(predicted_categories: List[str], ground_truth_categories: List[str]) -> Dict[str, float]:
    """
    Standard Precision, Recall aur F1-Score calculate karta hai.
    """
    pred_set: Set[str] = set(predicted_categories)
    true_set: Set[str] = set(ground_truth_categories)

    tp = len(pred_set & true_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "f1_score": round(f1, 3),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn
    }


if __name__ == "__main__":
    from src.parser import load_and_chunk_pdf
    from src.vectorstore import get_vector_store
    from src.analyzer import analyze_document_risks

    pdf_path = r"src\CognoDB-Assignment-2-Application.docx (1).pdf"
    
    # 1. Chunks load karo
    chunks = load_and_chunk_pdf(pdf_path)
    raw_text = " ".join([c.page_content for c in chunks])
    
    # 2. Vector DB aur analysis chalao
    v_db = get_vector_store(chunks)
    report = analyze_document_risks(v_db, document_name="CognoDB_Assignment.pdf")
    
    # 3. Groundedness test
    grounded_res = calculate_groundedness_score(report, raw_text)
    print("\n--- GROUNDEDNESS EVALUATION ---")
    print(grounded_res)
    
    # 4. Metrics test (Example ground truth ke against)
    # Agar document me koi actual legal risk nahi tha, toh true list empty ya minimal hogi
    ground_truth = [] 
    predicted = [item.category.value for item in report.risks_detected]
    
    metrics_res = calculate_risk_metrics(predicted, ground_truth)
    print("\n--- CLASSIFICATION METRICS ---")
    print(metrics_res)