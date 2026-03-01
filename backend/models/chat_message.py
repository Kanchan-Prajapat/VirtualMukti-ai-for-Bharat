from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ChatMessage(BaseModel):
    user_id: str
    sender: str  # "user" or "bot"
    text: str
    timestamp: datetime
    crisis_detected: Optional[bool] = False