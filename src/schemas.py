from enum import Enum
from typing import List
from pydantic import BaseModel, Field

class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class RiskCategory(str, Enum):
    LIABILITY = "Liability & Indemnification"
    TERMINATION = "Termination & Lock-in"
    DATA_PRIVACY = "Data Privacy & IP Ownership"
    PAYMENT = "Payment & Penalty Terms"
    JURISDICTION = "Jurisdiction & Compliance"

class RiskItem(BaseModel):
    category: RiskCategory
    level: SeverityLevel = Field(description="Severity level of the risk")
    clause_title: str = Field(description="Short title or clause reference")
    issue_description: str = Field(description="Specific legal or operational risk explained")
    verbatim_evidence: str = Field(description="Exact quote from the document text")
    recommended_mitigation: str = Field(description="Actionable suggestion to negotiate or fix")

class DocumentRiskReport(BaseModel): 
    document_name: str
    overall_risk_score: SeverityLevel
    summary: str = Field(description="High-level 2-3 sentence overview of the risk posture")
    risks_detected: List[RiskItem] = Field(default_factory=list)


if __name__ == "__main__":
    test_data = {
        "document_name": "vendor_nda.pdf",
        "overall_risk_score": "HIGH",
        "summary": "This agreement contains broad liability and indefinite confidentiality terms.",
        "risks_detected": [
            {
                "category": "Liability & Indemnification",
                "level": "HIGH",
                "clause_title": "Section 8.2 - Unlimited Liability",
                "issue_description": "Supplier holds unlimited liability for indirect damages.",
                "verbatim_evidence": "Supplier shall defend, indemnify and hold harmless without limitation...",
                "recommended_mitigation": "Cap liability to 12 months of service fees."
            }
        ]
    }
    
    report = DocumentRiskReport(**test_data)
    print("Validation Success!")
    print(report.model_dump_json(indent=2))