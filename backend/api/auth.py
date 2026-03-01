"""
Authentication API endpoints (Bearer Token based)
Production-ready version
"""

from fastapi import APIRouter, HTTPException, Depends, Header, status
from typing import Optional
import logging

from ..models.user import UserCreate, UserLogin
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository

router = APIRouter(tags=["Authentication"])
logger = logging.getLogger(__name__)


# =========================
# REGISTER
# =========================
@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    try:
        result = await AuthService.register(user_data)

        logger.info(f"User registered: {result['username']}")

        return {
            "success": True,
            "token": result["token"],
            "user_id": result["user_id"],
            "username": result["username"],
            "message": "Registration successful",
        }

    except ValueError as e:
        logger.warning(f"Registration conflict: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed",
        )


# =========================
# LOGIN
# =========================
@router.post("/login")
async def login(credentials: UserLogin):
    try:
        result = await AuthService.login(
            credentials.username,
            credentials.password
        )

        logger.info(f"User login: {result['username']}")

        return {
            "success": True,
            "token": result["token"],
            "user_id": result["user_id"],
            "username": result["username"],
            "message": "Login successful",
        }

    except ValueError as e:
        logger.warning(f"Invalid login attempt for: {credentials.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed",
        )


# =========================
# AUTH DEPENDENCY
# =========================
async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> dict:
    """
    Extract user from Authorization: Bearer <token>
    """

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )

    token = authorization.split(" ")[1]
    payload = AuthService.validate_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload


# =========================
# CURRENT USER
# =========================
@router.get("/me")
async def get_current_user_info(user: dict = Depends(get_current_user)):

    user_obj = await UserRepository.get_by_id(user["user_id"])

    if not user_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {
        "id": user_obj["id"],
        "username": user_obj["username"],
        "language_preference": user_obj.get("language_preference"),
        "addiction_type": user_obj.get("addiction_type"),
        "recovery_streak": user_obj.get("recovery_streak", 0),
    }