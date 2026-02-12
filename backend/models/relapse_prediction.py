from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# -----------------------------
# Risk Factor
# -----------------------------
class RiskFactor(BaseModel):
    name: str
    weight: float
    description: Optional[str] = None

    model_config = {
        "protected_namespaces": (),
    }


# -----------------------------
# DB Model
# -----------------------------
class RelapseRiskResponse(BaseModel):
    user_id: str
    prediction_date: datetime

    risk_score: float
    risk_level: str
    confidence: float

    top_risk_factors: List[RiskFactor]
    protective_factors: List[str]

    requires_intervention: bool
    explanation: str
    model_version: str

    model_config = {
        "protected_namespaces": (),
    }
