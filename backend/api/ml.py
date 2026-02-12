"""ML API endpoints for relapse risk prediction"""

from fastapi import APIRouter, HTTPException, Depends

from ..services.ml_service import MLService
from ..api.auth import get_current_user
from ..models.relapse_prediction import RelapseRiskResponse

router = APIRouter()


@router.get("/relapse-risk", response_model=RelapseRiskResponse)
async def get_relapse_risk(user: dict = Depends(get_current_user)):
    """
    Get daily relapse risk prediction for current user
    """
    try:
        return await MLService.predict_relapse_risk(user["user_id"])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate prediction: {str(e)}"
        )
