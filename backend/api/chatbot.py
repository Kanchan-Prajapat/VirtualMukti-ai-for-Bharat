"""Chatbot API endpoints"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from ..services.chatbot_service import ChatbotService
from ..api.auth import get_current_user

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message request"""
    message: str = Field(..., min_length=1, max_length=1000)
    language: str | None = Field(None, description="hindi, hinglish, or english (auto-detect if not provided)")


class ChatResponse(BaseModel):
    """Chat response"""
    response: str
    crisis_detected: bool
    language: str


@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_message: ChatMessage,
    user: dict = Depends(get_current_user)
):
    """
    Send message to CBT chatbot
    
    - **message**: User message (1-1000 chars)
    - **language**: Optional language preference (auto-detected if not provided)
    
    Returns:
    - **response**: Bot response with CBT techniques
    - **crisis_detected**: True if crisis keywords detected
    - **language**: Detected/used language
    """
    try:
        result = await ChatbotService.send_message(
            user_id=user["user_id"],
            message=chat_message.message,
            language=chat_message.language
        )
        
        return ChatResponse(
            response=result['response'],
            crisis_detected=result['crisis_detected'],
            language=result['language']
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process message: {str(e)}"
        )
