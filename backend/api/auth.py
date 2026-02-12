"""Authentication API endpoints (Bearer Token based)"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional
from datetime import datetime

from ..models.user import UserCreate, UserLogin, UserResponse
from ..services.auth_service import AuthService
from ..repositories.user_repository import UserRepository

router = APIRouter(tags=["auth"])

# =========================
# REGISTER
# =========================
@router.post("/register")
async def register(user_data: UserCreate):
    # 🔍 STEP 3A: LOG INPUT
    print("📥 REGISTER PAYLOAD RECEIVED:", user_data)

    try:
        result = await AuthService.register(user_data)

        return {
            "success": True,
            "token": result["token"],
            "user_id": result["user_id"],
            "username": result["username"],
            "message": "Registration successful",
        }

    except ValueError as e:
        print("❌ REGISTER VALUE ERROR:", e)
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        print("🔥 REGISTER INTERNAL ERROR:", e)
        raise HTTPException(status_code=500, detail="Registration failed")


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

        return {
            "success": True,
            "token": result["token"],
            "user_id": result["user_id"],
            "username": result["username"],
            "message": "Login successful",
        }

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Login failed")


# =========================
# AUTH DEPENDENCY
# =========================
async def get_current_user(
    authorization: str = Header(...)
) -> dict:
    """
    Extract user from Authorization: Bearer <token>
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = authorization.replace("Bearer ", "")
    payload = AuthService.validate_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload


# =========================
# CURRENT USER
# =========================
@router.get("/me")
async def me(user: dict = Depends(get_current_user)):
    user_obj = await UserRepository.get_by_id(user["user_id"])

    if not user_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return {
    "id": user_obj["id"],
    "username": user_obj["username"],
    "language_preference": user_obj.get("language_preference"),
    "addiction_type": user_obj.get("addiction_type"),
    "recovery_streak": user_obj.get("recovery_streak", 0),
}

