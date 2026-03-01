"""
Chatbot API endpoints
Production-ready version (MongoDB persistent)
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from ..services.chatbot_service import ChatbotService
from ..repositories.chat_repository import ChatRepository
from ..api.auth import get_current_user

router = APIRouter(tags=["Chatbot"])
logger = logging.getLogger(__name__)


# =====================================
# Request Models
# =====================================

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User message (1-1000 characters)"
    )

    language: Optional[str] = Field(
        None,
        description="hindi, hinglish, or english"
    )


# =====================================
# Response Models
# =====================================

class ChatResponse(BaseModel):
    response: str
    crisis_detected: bool
    language: str


class ChatHistoryResponse(BaseModel):
    user_id: str
    sender: str
    text: str
    timestamp: str
    crisis_detected: bool


# =====================================
# Send Message Endpoint
# =====================================

@router.post(
    "/message",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK
)
async def send_message(
    payload: ChatRequest,
    user: dict = Depends(get_current_user)
):
    """
    Send a message to AI recovery chatbot.
    """

    try:
        user_id = user["user_id"]

        logger.info(f"[CHAT] Incoming message from user={user_id}")

        result = await ChatbotService.send_message(
            user_id=user_id,
            message=payload.message.strip(),
            language=payload.language
        )

        if result.get("crisis_detected"):
            logger.warning(f"[CRISIS] Detected for user={user_id}")

        return ChatResponse(
            response=result["response"],
            crisis_detected=result["crisis_detected"],
            language=result["language"]
        )

    except Exception as e:
        logger.error(f"[CHAT ERROR] user={user.get('user_id')} error={e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process message"
        )


# =====================================
# Get Chat History
# =====================================

@router.get(
    "/history",
    response_model=List[ChatHistoryResponse],
    status_code=status.HTTP_200_OK
)
async def get_chat_history(
    user: dict = Depends(get_current_user)
):
    """
    Fetch full chat history for authenticated user.
    """

    try:
        user_id = user["user_id"]

        messages = await ChatRepository.get_messages(user_id)

        return [
            ChatHistoryResponse(
                user_id=m["user_id"],
                sender=m["sender"],
                text=m["text"],
                timestamp=m["timestamp"].isoformat(),
                crisis_detected=m.get("crisis_detected", False)
            )
            for m in messages
        ]

    except Exception as e:
        logger.error(f"[CHAT HISTORY ERROR] user={user.get('user_id')} error={e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch chat history"
        )


# =====================================
# Clear Chat History
# =====================================

@router.delete(
    "/history",
    status_code=status.HTTP_200_OK
)
async def clear_chat_history(
    user: dict = Depends(get_current_user)
):
    """
    Clear entire chat history for user.
    """

    try:
        user_id = user["user_id"]

        await ChatRepository.clear_messages(user_id)

        logger.info(f"[CHAT CLEARED] user={user_id}")

        return {"success": True, "message": "Chat history cleared"}

    except Exception as e:
        logger.error(f"[CHAT CLEAR ERROR] user={user.get('user_id')} error={e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear chat history"
        )