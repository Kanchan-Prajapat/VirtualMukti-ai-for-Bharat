"""
ML API endpoints for relapse risk prediction
Production-ready version
"""

from fastapi import APIRouter, HTTPException, Depends, status
import logging

from ..services.ml_service import MLService
from ..api.auth import get_current_user
from ..models.relapse_prediction import RelapseRiskResponse

router = APIRouter(tags=["Machine Learning"])
logger = logging.getLogger(__name__)


@router.get(
    "/relapse-risk",
    response_model=RelapseRiskResponse,
    status_code=status.HTTP_200_OK
)
async def get_relapse_risk(user: dict = Depends(get_current_user)):
    """
    Get daily relapse risk prediction for authenticated user
    """

    try:
        logger.info(f"Generating relapse prediction for user {user['user_id']}")

        prediction = await MLService.predict_relapse_risk(
            user["user_id"]
        )

        return prediction

    except ValueError as e:
        logger.warning(f"ML validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:
        logger.error(f"Relapse prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate relapse prediction"
        )