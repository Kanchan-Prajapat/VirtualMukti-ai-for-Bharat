"""User activity models"""

from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field


# ---------------------------
# Base Activity Model
# ---------------------------
class UserActivity(BaseModel):
    user_id: str
    date: date

    mood_score: int = Field(ge=1, le=10)
    craving_intensity: int = Field(ge=0, le=10)

    triggers_encountered: List[str] = []
    coping_strategies_used: List[str] = []

    flows_completed: List[str] = []
    exercises_completed: List[str] = []

    chatbot_sessions: int = 0
    messages_sent: int = 0
    sos_triggered: bool = False

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


# ---------------------------
# Create Schema
# ---------------------------
class UserActivityCreate(BaseModel):
    mood_score: int = Field(ge=1, le=10)
    craving_intensity: int = Field(ge=0, le=10)

    triggers_encountered: List[str] = []
    coping_strategies_used: List[str] = []


# ---------------------------
# Update Schema
# ---------------------------
class UserActivityUpdate(BaseModel):
    mood_score: Optional[int] = Field(default=None, ge=1, le=10)
    craving_intensity: Optional[int] = Field(default=None, ge=0, le=10)

    triggers_encountered: Optional[List[str]] = None
    coping_strategies_used: Optional[List[str]] = None

    flows_completed: Optional[List[str]] = None
    exercises_completed: Optional[List[str]] = None

    chatbot_sessions: Optional[int] = None
    messages_sent: Optional[int] = None
    sos_triggered: Optional[bool] = None
