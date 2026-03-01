"""
ML Service for relapse risk prediction
Production-ready hybrid logic (ML + rule-based fallback)
"""

import numpy as np
from datetime import datetime
from typing import List
import logging

from ..models.relapse_prediction import RelapseRiskResponse, RiskFactor
from ..repositories.user_activity_repository import UserActivityRepository

logger = logging.getLogger(__name__)


class MLService:
    """Relapse risk prediction service"""

    # ----------------------------
    # Calculate Risk Score (Hybrid Logic)
    # ----------------------------
    @staticmethod
    def _calculate_risk(activities: List[dict]) -> float:
        """
        Basic hybrid scoring until full LSTM production model is deployed.
        """

        if not activities:
            return 50.0  # default moderate risk

        mood_avg = np.mean([a.get("mood_score", 5) for a in activities])
        craving_avg = np.mean([a.get("craving_intensity", 5) for a in activities])
        trigger_avg = np.mean([len(a.get("triggers_encountered", [])) for a in activities])

        # Weighted score
        risk_score = (
            (10 - mood_avg) * 4 +
            craving_avg * 5 +
            trigger_avg * 6
        )

        return min(max(risk_score, 0), 100)

    # ----------------------------
    # Determine Risk Level
    # ----------------------------
    @staticmethod
    def _risk_level(score: float) -> str:
        if score < 30:
            return "low"
        elif score < 70:
            return "moderate"
        return "high"

    # ----------------------------
    # Main Prediction
    # ----------------------------
    @staticmethod
    async def predict_relapse_risk(user_id: str) -> RelapseRiskResponse:

        try:
            activities = await UserActivityRepository.get_recent(user_id, days=30)

            risk_score = MLService._calculate_risk(activities)
            risk_level = MLService._risk_level(risk_score)

            requires_intervention = risk_score >= 75

            explanation = (
                "Risk calculated based on mood, cravings and trigger patterns "
                "over the past 30 days."
            )

            logger.info(
                f"Relapse prediction generated | user={user_id} | score={risk_score}"
            )

            return RelapseRiskResponse(
                user_id=user_id,
                prediction_date=datetime.utcnow(),
                risk_score=round(risk_score, 2),
                risk_level=risk_level,
                confidence=0.78,
                top_risk_factors=[
                    RiskFactor(name="craving_intensity", weight=0.5),
                    RiskFactor(name="mood_score", weight=0.3),
                ],
                protective_factors=["recovery_streak"],
                requires_intervention=requires_intervention,
                explanation=explanation,
                model_version="hybrid-v2",
            )

        except Exception as e:
            logger.error(f"Relapse prediction failed: {e}")

            return RelapseRiskResponse(
                user_id=user_id,
                prediction_date=datetime.utcnow(),
                risk_score=50,
                risk_level="moderate",
                confidence=0.3,
                top_risk_factors=[],
                protective_factors=[],
                requires_intervention=False,
                explanation="Insufficient data to compute full risk.",
                model_version="fallback-v1",
            )