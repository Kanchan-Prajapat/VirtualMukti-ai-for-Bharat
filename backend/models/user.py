from pydantic import BaseModel, Field, EmailStr
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime


# -----------------------------
# Demographics
# -----------------------------
class Demographics(BaseModel):
    age: int
    gender: str
    location: str
    addiction_type: str
    severity: str

    model_config = {
        "protected_namespaces": (),
    }


# -----------------------------
# Base User (DB model)
# -----------------------------
class User(BaseModel):
    id: str
    username: str
    password_hash: str
    demographics: Demographics

    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    recovery_start_date: Optional[datetime] = None

    language_preference: Optional[str] = "en"
    addiction_type: Optional[str] = None
    recovery_streak: int = 0

    data_encrypted: bool = True
    consent_given: bool

    model_config = {
        "from_attributes": True,
        "protected_namespaces": (),
    }


# -----------------------------
# User Registration
# -----------------------------
class UserCreate(BaseModel):
    username: str
    password: str
    demographics: Demographics
    language_preference: Optional[str] = "en"
    consent_given: bool

    model_config = {
        "protected_namespaces": (),
    }


# -----------------------------
# User Login
# ✅ THIS WAS MISSING
# -----------------------------
class UserLogin(BaseModel):
    username: str
    password: str

    model_config = {
        "protected_namespaces": (),
    }


# -----------------------------
# User API Response (SAFE)
# -----------------------------
class UserResponse(BaseModel):
    id: str
    username: str
    demographics: Demographics
    recovery_streak: int
    addiction_type: Optional[str]
    language_preference: Optional[str]

    model_config = {
        "protected_namespaces": (),
    }
