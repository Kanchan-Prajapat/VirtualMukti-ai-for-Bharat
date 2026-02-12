# """Chatbot service with Gemini integration and CBT techniques"""

# import google.generativeai as genai
# from typing import Optional
# import logging

# from ..config import settings

# logger = logging.getLogger(__name__)

# # Configure Gemini
# genai.configure(api_key=settings.gemini_api_key)


# class ChatbotService:
#     """CBT-based chatbot service using Gemini"""
    
#     # Crisis keywords for detection
#     CRISIS_KEYWORDS = [
#         'suicide', 'kill myself', 'end my life', 'want to die',
#         'आत्महत्या', 'मरना चाहता', 'जीना नहीं चाहता',
#         'harm myself', 'hurt myself', 'no reason to live'
#     ]
    
#     # CBT system prompt
#     CBT_SYSTEM_PROMPT = """You are a compassionate AI counselor specializing in addiction recovery support using Cognitive Behavioral Therapy (CBT) techniques. 

# Your role:
# - Provide supportive, non-judgmental responses
# - Use CBT techniques: cognitive reframing, behavioral activation, identifying triggers
# - Respond in Hindi, Hinglish, or English based on user's language
# - Keep responses concise (2-3 sentences)
# - Focus on coping strategies and positive reinforcement
# - Never provide medical advice or replace professional treatment

# CBT Techniques to use:
# 1. Cognitive Reframing: Help identify and challenge negative thoughts
# 2. Behavioral Activation: Encourage positive activities
# 3. Trigger Identification: Help recognize and manage triggers
# 4. Coping Strategies: Suggest healthy alternatives to substance use

# If user shows signs of crisis (suicidal thoughts, severe distress), acknowledge their pain and strongly encourage professional help.

# Be warm, empathetic, and culturally sensitive to Indian context."""
    
#     @staticmethod
#     def detect_crisis(message: str) -> bool:
#         """
#         Detect crisis keywords in message
        
#         Args:
#             message: User message
            
#         Returns:
#             True if crisis detected
#         """
#         message_lower = message.lower()
#         for keyword in ChatbotService.CRISIS_KEYWORDS:
#             if keyword in message_lower:
#                 logger.warning(f"Crisis keyword detected: {keyword}")
#                 return True
#         return False
    
#     @staticmethod
#     def detect_language(message: str) -> str:
#         """
#         Simple language detection
        
#         Args:
#             message: User message
            
#         Returns:
#             'hindi', 'hinglish', or 'english'
#         """
#         # Check for Devanagari script
#         if any('\u0900' <= char <= '\u097F' for char in message):
#             return 'hindi'
        
#         # Check for common Hinglish patterns
#         hinglish_words = ['hai', 'hoon', 'kya', 'nahi', 'acha', 'theek']
#         if any(word in message.lower() for word in hinglish_words):
#             return 'hinglish'
        
#         return 'english'
    
#     @staticmethod
#     async def send_message(user_id: str, message: str, language: Optional[str] = None) -> dict:
#         """
#         Process user message and generate CBT-based response
        
#         Args:
#             user_id: User identifier
#             message: User message
#             language: Preferred language (auto-detect if None)
            
#         Returns:
#             Dict with response, crisis_detected, language
#         """
#         # Detect crisis
#         crisis_detected = ChatbotService.detect_crisis(message)
        
#         # Detect language if not provided
#         if not language:
#             language = ChatbotService.detect_language(message)
        
#         # Build prompt with language instruction
#         language_instruction = {
#             'hindi': 'Respond in Hindi (Devanagari script).',
#             'hinglish': 'Respond in Hinglish (Hindi words in Roman script mixed with English).',
#             'english': 'Respond in English.'
#         }
        
#         full_prompt = f"{ChatbotService.CBT_SYSTEM_PROMPT}\n\n{language_instruction[language]}\n\nUser message: {message}\n\nYour response:"
        
#         try:
#             # Call Gemini API
#             model = genai.GenerativeModel(
#     model_name="models/gemini-1.5-flash"
# )
#             response = model.generate_content(full_prompt)
            
#             bot_response = response.text.strip()

#             for m in genai.list_models():
#              if "generateContent" in m.supported_generation_methods:
#                print(m.name)
            
#             # If crisis detected, add crisis resources
#             if crisis_detected:
#                 crisis_addendum = {
#                     'hindi': '\n\nकृपया तुरंत मदद लें: NIMHANS हेल्पलाइन 080-46110007',
#                     'hinglish': '\n\nPlease seek immediate help: NIMHANS Helpline 080-46110007',
#                     'english': '\n\nPlease seek immediate help: NIMHANS Helpline 080-46110007'
#                 }
#                 bot_response += crisis_addendum[language]
            
#             logger.info(f"Generated response for user {user_id}, crisis={crisis_detected}")
            
#             return {
#                 'response': bot_response,
#                 'crisis_detected': crisis_detected,
#                 'language': language
#             }
        
#         except Exception as e:
#             logger.error(f"Gemini API error: {e}")
            
#             # Fallback response
#             fallback_responses = {
#                 'hindi': 'मुझे खेद है, मैं अभी उपलब्ध नहीं हूं। कृपया बाद में पुनः प्रयास करें।',
#                 'hinglish': 'Sorry, main abhi available nahi hoon. Please try again later.',
#                 'english': 'Sorry, I am not available right now. Please try again later.'
#             }
            
#             return {
#                 'response': fallback_responses[language],
#                 'crisis_detected': crisis_detected,
#                 'language': language,
#                 'error': str(e)
#             }

import logging
from typing import Optional
import google.generativeai as genai

from ..config import settings

logger = logging.getLogger(__name__)

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)


def get_working_gemini_model():
    """
    Dynamically select a Gemini model that supports generateContent.
    This avoids hardcoding model names (PERMANENT FIX).
    """
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            logger.info(f"Using Gemini model: {model.name}")
            return genai.GenerativeModel(model.name)

    raise RuntimeError("No Gemini model supports generateContent for this API key")


class ChatbotService:
    CRISIS_KEYWORDS = [
        "suicide", "kill myself", "end my life", "want to die",
        "harm myself", "no reason to live",
        "आत्महत्या", "मरना चाहता", "जीना नहीं चाहता"
    ]

    CBT_SYSTEM_PROMPT = (
        "You are a compassionate AI counselor specializing in addiction recovery "
        "using Cognitive Behavioral Therapy (CBT). Keep responses short, supportive, "
        "and culturally sensitive to India."
    )

    _model = get_working_gemini_model()

    @staticmethod
    def detect_crisis(message: str) -> bool:
        text = message.lower()
        return any(k in text for k in ChatbotService.CRISIS_KEYWORDS)

    @staticmethod
    async def send_message(
        user_id: str,
        message: str,
        language: Optional[str] = None
    ) -> dict:

        crisis = ChatbotService.detect_crisis(message)

        prompt = f"""
{ChatbotService.CBT_SYSTEM_PROMPT}

User message:
{message}

Respond empathetically.
"""

        try:
            response = ChatbotService._model.generate_content(prompt)
            text = response.text.strip()

            if crisis:
                text += (
                    "\n\nIf you are in India, please contact NIMHANS Helpline: "
                    "080-46110007 or reach out to someone you trust."
                )

            return {
                "response": text,
                "crisis_detected": crisis,
                "language": language or "english"
            }

        except Exception as e:
            logger.error(f"Gemini API error: {e}")

            return {
                "response": "Sorry, I’m having trouble right now. Please try again shortly.",
                "crisis_detected": crisis,
                "language": language or "english"
            }
