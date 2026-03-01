"""
Chatbot service with Gemini integration
Production-ready version
"""

import logging
from typing import Optional
import google.generativeai as genai

from ..repositories.chat_repository import ChatRepository
from ..config import settings

logger = logging.getLogger(__name__)

# Configure Gemini once
genai.configure(api_key=settings.gemini_api_key)


class ChatbotService:
    """
    AI-powered CBT chatbot service
    """

    CRISIS_KEYWORDS = [
        "suicide", "kill myself", "end my life", "want to die",
        "harm myself", "hurt myself", "no reason to live",
        "आत्महत्या", "मरना चाहता", "जीना नहीं चाहता"
    ]

    CBT_SYSTEM_PROMPT = """
You are a compassionate AI counselor specializing in addiction recovery using Cognitive Behavioral Therapy (CBT).

Rules:
- Keep responses short (2–4 sentences)
- Be warm and empathetic
- Never give medical advice
- Encourage healthy coping
- Be culturally sensitive to India
"""

    _model = None

    # -------------------------
    # Lazy model loading
    # -------------------------
    @classmethod
    def get_model(cls):
        if cls._model is None:
            try:
                for m in genai.list_models():
                    if "generateContent" in m.supported_generation_methods:
                        logger.info(f"Using Gemini model: {m.name}")
                        cls._model = genai.GenerativeModel(m.name)
                        break

                if cls._model is None:
                    raise RuntimeError("No compatible Gemini model found.")

            except Exception as e:
                logger.error(f"Failed to initialize Gemini model: {e}")
                raise

        return cls._model

    # -------------------------
    # Crisis Detection
    # -------------------------
    @staticmethod
    def detect_crisis(message: str) -> bool:
        text = message.lower()
        return any(keyword in text for keyword in ChatbotService.CRISIS_KEYWORDS)

    # -------------------------
    # Language Detection
    # -------------------------
    @staticmethod
    def detect_language(message: str) -> str:
        if any('\u0900' <= char <= '\u097F' for char in message):
            return "hindi"

        hinglish_words = ["hai", "hoon", "kya", "nahi", "acha", "theek"]
        if any(word in message.lower() for word in hinglish_words):
            return "hinglish"

        return "english"

    # -------------------------
    # Send Message
    # -------------------------
    @staticmethod
    async def send_message(
        user_id: str,
        message: str,
        language: Optional[str] = None
    ):

        # Detect crisis
        crisis = ChatbotService.detect_crisis(message)

        # Detect language if not provided
        if not language:
            language = ChatbotService.detect_language(message)

        # Save user message
        await ChatRepository.save_message(
            user_id=user_id,
            sender="user",
            text=message,
            crisis_detected=False
        )

        prompt = f"""
{ChatbotService.CBT_SYSTEM_PROMPT}

User message:
{message}

Respond empathetically.
"""

        try:
            model = ChatbotService.get_model()
            response = model.generate_content(prompt)
            text = response.text.strip()

            if crisis:
                text += (
                    "\n\nIf you are in India, please contact "
                    "NIMHANS Helpline: 080-46110007 "
                    "or reach out to someone you trust."
                )

            # Save bot message
            await ChatRepository.save_message(
                user_id=user_id,
                sender="bot",
                text=text,
                crisis_detected=crisis
            )

            return {
                "response": text,
                "crisis_detected": crisis,
                "language": language
            }

        except Exception as e:
            logger.error(f"Gemini error: {e}")

            fallback = (
                "Sorry, I’m having trouble responding right now. "
                "Please try again shortly."
            )

            # Save fallback message
            await ChatRepository.save_message(
                user_id=user_id,
                sender="bot",
                text=fallback,
                crisis_detected=False
            )

            return {
                "response": fallback,
                "crisis_detected": crisis,
                "language": language
            }