from typing import List, Optional
from pydantic import BaseModel

class RiskDetail(BaseModel):
    pattern: str
    message: str
    severity: str
    category: str

class RiskAssessmentMetadata(BaseModel):
    issues: int
    warnings: int
    infos: int
    criticals: int

class RiskAssessmentResult(BaseModel):
    risk_assessment: str
    risk_score: float
    total_risks: int
    risk_details: List[RiskDetail]
    risk_categories: List[str]
    prompt_used: str
    metadata: RiskAssessmentMetadata
    status: str
    error: Optional[str] = None
