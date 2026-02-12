"""ML Service for relapse risk prediction"""

import numpy as np
from datetime import datetime
from typing import List
import logging

from ..ml.lstm_model import lstm_model
from ..models.relapse_prediction import  RelapseRiskResponse, RiskFactor
from ..models.user_activity import UserActivity
from ..repositories.user_activity_repository import UserActivityRepository
# from ..repositories.relapse_prediction_repository import RelapseRiskRepository

logger = logging.getLogger(__name__)


class MLService:
    """Service for ML-based relapse prediction"""
    
    @staticmethod
    def _prepare_sequence(activities: List[UserActivity]) -> np.ndarray:
        """
        Convert user activities to LSTM input sequence
        
        Args:
            activities: List of UserActivity objects (should be 30 days)
            
        Returns:
            Numpy array of shape (30, 6)
        """
        sequence = []
        
        for activity in activities:
            # Extract features in correct order
            features = [
                activity.mood_score,
                activity.craving_intensity,
                len(activity.triggers_encountered),
                len(activity.flows_completed),
                activity.chatbot_sessions,
                0  # recovery_streak (will be set from user)
            ]
            sequence.append(features)
        
        # Pad if less than 30 days
        while len(sequence) < 30:
            # Use neutral values for missing days
            sequence.insert(0, [5, 5, 0, 0, 0, 0])
        
        # Truncate if more than 30 days
        sequence = sequence[-30:]
        
        return np.array(sequence)
    
    @staticmethod
    def _generate_explanation(risk_score: float, top_factors: list) -> List[str]:
        """
        Generate simple human-readable explanation
        
        Args:
            risk_score: Risk score 0-100
            top_factors: Top 2 risk factors
            
        Returns:
            List of explanation strings
        """
        explanations = []
        
        # Risk level
        if risk_score < 30:
            explanations.append("Your relapse risk is low. Keep up the good work!")
        elif risk_score < 70:
            explanations.append("Your relapse risk is moderate. Stay vigilant.")
        else:
            explanations.append("Your relapse risk is high. Consider reaching out for support.")
        
        # Top factors
        for factor_name, importance, value in top_factors[:2]:
            if factor_name == 'mood_score':
                if value < 5:
                    explanations.append(f"Low mood scores (avg {value:.1f}/10) are concerning.")
            elif factor_name == 'craving_intensity':
                if value > 5:
                    explanations.append(f"High craving intensity (avg {value:.1f}/10) needs attention.")
            elif factor_name == 'triggers_count':
                if value > 2:
                    explanations.append(f"Frequent triggers (avg {value:.1f}/day) detected.")
            elif factor_name == 'flows_completed':
                if value < 0.5:
                    explanations.append("Low completion of daily recovery flows.")
            elif factor_name == 'chatbot_engagement':
                if value < 1:
                    explanations.append("Consider engaging more with the support chatbot.")
        
        return explanations
    
    # @staticmethod
    # async def predict_relapse_risk(user_id: str) -> RelapseRiskPrediction:
    #     """
    #     Generate relapse risk prediction for user
        
    #     Args:
    #         user_id: User identifier
            
    #     Returns:
    #         RelapseRiskPrediction object
    #     """
    #     # Ensure model is trained
    #     if not lstm_model.is_trained:
    #         logger.info("Training LSTM model with synthetic data...")
    #         lstm_model.train_with_synthetic_data(num_samples=1000)
        
    #     # Get last 30 days of activity
    #     activities = await UserActivityRepository.get_recent(user_id, days=30)
        
    #     if not activities:
    #         # No activity data - return default moderate risk
    #         logger.warning(f"No activity data for user {user_id}, returning default prediction")
    #         return RelapseRiskPrediction(
    #             user_id=user_id,
    #             risk_score=50.0,
    #             confidence=0.3,
    #             top_risk_factors=[
    #                 RiskFactor(
    #                     factor_name="insufficient_data",
    #                     importance=1.0,
    #                     description="Not enough activity data for accurate prediction"
    #                 )
    #             ],
    #             protective_factors=[],
    #             model_version="lstm_v1.0.0",
    #             features_used=lstm_model.FEATURES
    #         )
        
    #     # Prepare sequence
    #     sequence = MLService._prepare_sequence(activities)
        
    #     # Get prediction
    #     risk_score = lstm_model.predict(sequence)
        
    #     # Get feature importance
    #     importances = lstm_model.get_feature_importance(sequence)
        
    #     # Create risk factors from top 2
    #     top_risk_factors = []
    #     for factor_name, importance, value in importances[:2]:
    #         top_risk_factors.append(
    #             RiskFactor(
    #                 factor_name=factor_name,
    #                 importance=float(importance),
    #                 description=f"Recent average: {value:.2f}"
    #             )
    #         )
        
    #     # Identify protective factors
    #     protective_factors = []
    #     for factor_name, importance, value in importances:
    #         if factor_name == 'mood_score' and value >= 7:
    #             protective_factors.append("good_mood")
    #         elif factor_name == 'craving_intensity' and value <= 3:
    #             protective_factors.append("low_cravings")
    #         elif factor_name == 'flows_completed' and value >= 0.7:
    #             protective_factors.append("consistent_daily_flows")
    #         elif factor_name == 'chatbot_engagement' and value >= 2:
    #             protective_factors.append("active_chatbot_engagement")
    #         elif factor_name == 'recovery_streak' and value >= 30:
    #             protective_factors.append("strong_recovery_streak")
        
    #     # Create prediction object
    #     prediction = RelapseRiskPrediction(
    #         user_id=user_id,
    #         risk_score=risk_score,
    #         confidence=0.85,  # Fixed confidence for MVP
    #         top_risk_factors=top_risk_factors,
    #         protective_factors=protective_factors,
    #         model_version="lstm_v1.0.0",
    #         features_used=lstm_model.FEATURES
    #     )
        
    #     # Store prediction
    #     await RelapseRiskRepository.create(prediction)
        
    #     logger.info(f"Generated prediction for user {user_id}: risk_score={risk_score:.2f}")
        
    #     return prediction
    @staticmethod
    async def predict_relapse_risk(user_id: str):
        return RelapseRiskResponse(
            user_id=user_id,
            prediction_date=datetime.utcnow(),
            risk_score=42,
            risk_level="moderate",
            confidence=0.82,
            top_risk_factors=[
                RiskFactor(name="craving_intensity", weight=0.6),
                RiskFactor(name="mood_score", weight=0.4),
            ],
            protective_factors=["recovery_streak"],
            requires_intervention=False,
            explanation="Moderate risk due to cravings, offset by recovery progress.",
            model_version="mock-v1",
        )
