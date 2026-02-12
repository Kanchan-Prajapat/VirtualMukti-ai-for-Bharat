"""User activity repository for database operations"""

from typing import Optional, List
from datetime import datetime, date
import logging

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import IndexModel, ASCENDING

from ..database import db
from ..models.user_activity import (
    UserActivity,
    UserActivityCreate,
    UserActivityUpdate,
)

logger = logging.getLogger(__name__)


class UserActivityRepository:
    """Repository for UserActivity collection operations"""

    COLLECTION_NAME = "user_activities"

    # ---------------------------
    # Collection
    # ---------------------------
    @classmethod
    def get_collection(cls) -> AsyncIOMotorCollection:
        return db.get_collection(cls.COLLECTION_NAME)

    # ---------------------------
    # Indexes
    # ---------------------------
    @classmethod
    async def create_indexes(cls) -> None:
        collection = cls.get_collection()

        indexes = [
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("user_id", ASCENDING), ("date", ASCENDING)], unique=True),
            IndexModel([("created_at", ASCENDING)]),
        ]

        await collection.create_indexes(indexes)
        logger.info("UserActivity indexes created")

    # ---------------------------
    # Create
    # ---------------------------
    @classmethod
    async def create_activity(
        cls, user_id: str, data: UserActivityCreate
    ) -> dict:
        collection = cls.get_collection()

        today = date.today()

        activity_doc = {
            "user_id": user_id,
            "date": today,
            "mood_score": data.mood_score,
            "craving_intensity": data.craving_intensity,
            "triggers_encountered": data.triggers_encountered,
            "coping_strategies_used": data.coping_strategies_used,
            "flows_completed": [],
            "exercises_completed": [],
            "chatbot_sessions": 0,
            "messages_sent": 0,
            "sos_triggered": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        await collection.insert_one(activity_doc)
        logger.info(f"Activity created for user {user_id}")

        return activity_doc

    # ---------------------------
    # Read
    # ---------------------------
    @classmethod
    async def get_by_user_and_date(
        cls, user_id: str, activity_date: date
    ) -> Optional[dict]:
        collection = cls.get_collection()
        return await collection.find_one(
            {"user_id": user_id, "date": activity_date}
        )

    @classmethod
    async def get_recent_activities(
        cls, user_id: str, limit: int = 7
    ) -> List[dict]:
        collection = cls.get_collection()

        cursor = (
            collection.find({"user_id": user_id})
            .sort("date", -1)
            .limit(limit)
        )

        return await cursor.to_list(length=limit)

    # ---------------------------
    # Update
    # ---------------------------
    @classmethod
    async def update_activity(
        cls, user_id: str, activity_date: date, data: UserActivityUpdate
    ) -> bool:
        collection = cls.get_collection()

        update_data = {
            k: v for k, v in data.model_dump(exclude_unset=True).items()
        }

        if not update_data:
            return False

        update_data["updated_at"] = datetime.utcnow()

        result = await collection.update_one(
            {"user_id": user_id, "date": activity_date},
            {"$set": update_data},
        )

        return result.modified_count > 0

    # ---------------------------
    # Delete
    # ---------------------------
    @classmethod
    async def delete_activity(cls, user_id: str, activity_date: date) -> bool:
        collection = cls.get_collection()

        result = await collection.delete_one(
            {"user_id": user_id, "date": activity_date}
        )

        return result.deleted_count > 0
