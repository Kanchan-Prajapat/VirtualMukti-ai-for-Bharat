"""User repository for database operations"""

from typing import Optional
from datetime import datetime
import uuid
import logging

from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import IndexModel, ASCENDING
from pymongo.errors import DuplicateKeyError

from ..database import db
from ..models.user import User, Demographics
from ..encryption import encryption_service

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for User collection operations"""

    COLLECTION_NAME = "users"

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
            IndexModel([("username", ASCENDING)], unique=True),
            IndexModel([("id", ASCENDING)], unique=True),
            IndexModel([("created_at", ASCENDING)]),
            IndexModel([("last_login", ASCENDING)]),
        ]

        await collection.create_indexes(indexes)
        logger.info("User indexes created")

    # ---------------------------
    # Encryption helpers
    # ---------------------------
    @classmethod
    def _encrypt_demographics(cls, demographics: Demographics) -> dict:
        data = demographics.model_dump()

        return {
            "age": encryption_service.encrypt(str(data["age"])),
            "gender": encryption_service.encrypt(data["gender"]),
            "location": encryption_service.encrypt(data["location"]),
            "addiction_type": data["addiction_type"],
            "severity": data["severity"],
        }

    @classmethod
    def _decrypt_demographics(cls, encrypted: dict) -> Demographics:
        return Demographics(
            age=int(encryption_service.decrypt(encrypted["age"])),
            gender=encryption_service.decrypt(encrypted["gender"]),
            location=encryption_service.decrypt(encrypted["location"]),
            addiction_type=encrypted["addiction_type"],
            severity=encrypted["severity"],
        )

    # ---------------------------
    # Create user
    # ---------------------------
    @classmethod
    async def create(cls, user: User, password_hash: str) -> dict:
        collection = cls.get_collection()

        print("🧩 CREATING USER:", user.username)
        print("🧩 DEMOGRAPHICS:", user.demographics)

        user_id = str(uuid.uuid4())

        encrypted_demographics = cls._encrypt_demographics(user.demographics)

        user_doc = {
            "id": user_id,
            "username": user.username.lower(),
            "password_hash": password_hash,
            "demographics": encrypted_demographics,
            "created_at": datetime.utcnow(),
            "last_login": datetime.utcnow(),
            "language_preference": user.language_preference,
            "recovery_start_date": datetime.utcnow(),
            "addiction_type": user.demographics.addiction_type,
            "recovery_streak": 0,
            "data_encrypted": True,
            "consent_given": user.consent_given,
        }

        print("🧩 FINAL USER DOC (before insert):", user_doc)

        try:
            await collection.insert_one(user_doc)
            print("✅ USER INSERTED INTO DB:", user_id)
            return user_doc

        except DuplicateKeyError:
            print("❌ USERNAME ALREADY EXISTS:", user.username)
            raise ValueError("Username already exists")

        except Exception as e:
            print("🔥 DB INSERT FAILED:", e)
            raise

    # ---------------------------
    # Read
    # ---------------------------
    @classmethod
    async def get_by_username(cls, username: str) -> Optional[User]:
        collection = cls.get_collection()
        doc = await collection.find_one({"username": username.lower()})

        if not doc:
            return None

        demographics = cls._decrypt_demographics(doc["demographics"])

        return User(
            id=doc["id"],
            username=doc["username"],
            password_hash=doc["password_hash"],
            demographics=demographics,
            language_preference=doc["language_preference"],
            addiction_type=doc["addiction_type"],
            recovery_streak=doc["recovery_streak"],
            created_at=doc["created_at"],
            last_login=doc["last_login"],
            consent_given=doc["consent_given"],
        )

    @classmethod
    async def get_by_id(cls, user_id: str) -> Optional[dict]:
        collection = cls.get_collection()
        return await collection.find_one({"id": user_id})

    # ---------------------------
    # Updates
    # ---------------------------
    @classmethod
    async def update_last_login(cls, user_id: str) -> bool:
        collection = cls.get_collection()
        result = await collection.update_one(
            {"id": user_id},
            {"$set": {"last_login": datetime.utcnow()}},
        )
        return result.modified_count > 0

    @classmethod
    async def update_recovery_streak(cls, user_id: str, streak: int) -> bool:
        collection = cls.get_collection()
        result = await collection.update_one(
            {"id": user_id},
            {"$set": {"recovery_streak": streak}},
        )
        return result.modified_count > 0

    # ---------------------------
    # Delete
    # ---------------------------
    @classmethod
    async def delete(cls, user_id: str) -> bool:
        collection = cls.get_collection()
        result = await collection.delete_one({"id": user_id})
        return result.deleted_count > 0

    # ---------------------------
    # Utils
    # ---------------------------
    @classmethod
    async def username_exists(cls, username: str) -> bool:
        collection = cls.get_collection()
        count = await collection.count_documents({"username": username.lower()})
        return count > 0
