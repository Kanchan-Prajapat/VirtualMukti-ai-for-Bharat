from datetime import datetime
from typing import List
from bson import ObjectId

from ..database import db


class ChatRepository:

    COLLECTION = "chat_messages"

    @staticmethod
    async def save_message(
        user_id: str,
        sender: str,
        text: str,
        crisis_detected: bool = False
    ):
        collection = db.get_collection(ChatRepository.COLLECTION)

        document = {
            "user_id": user_id,
            "sender": sender,
            "text": text,
            "crisis_detected": crisis_detected,
            "timestamp": datetime.utcnow()
        }

        await collection.insert_one(document)

    @staticmethod
    async def get_user_messages(user_id: str) -> List[dict]:
        collection = db.get_collection(ChatRepository.COLLECTION)

        cursor = collection.find(
            {"user_id": user_id}
        ).sort("timestamp", 1)

        messages = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            doc.pop("_id", None)
            messages.append(doc)

        return messages