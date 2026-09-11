from typing import Any, Optional
from pydantic import BaseModel, Field

class ComplaintInput(BaseModel):
    source: str = "Manual"
    customer_name: str = ""
    product_name: str = ""
    batch_number: str = ""
    dosage_form: str = ""
    market: str = ""
    complaint_date: str = ""
    description: str = Field(min_length=3)

class AIAnalysis(BaseModel):
    extracted: dict[str, Any]
    summary: str
    completeness_score: int
    missing_fields: list[str]
    risk_level: str
    risk_score: int
    risk_rationale: str
    root_cause_recommendations: list[str]
    capa_recommendations: list[str]
    duplicate_risk: str = "Low"
    duplicate_reason: str = ""

class ComplaintResponse(ComplaintInput):
    id: int
    complaint_number: str
    summary: Optional[str] = None
    risk_level: Optional[str] = None
    risk_score: Optional[int] = None
    risk_rationale: Optional[str] = None
    ai_analysis: Optional[dict] = None
    status: str
    created_at: str
