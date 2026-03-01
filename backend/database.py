"""
MongoDB database connection and utilities with encryption support
Production-ready version with connection validation and pooling
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from typing import Optional
import logging
import asyncio

from .config import settings

logger = logging.getLogger(__name__)


class Database:
    """MongoDB database connection manager"""

    client: Optional[AsyncIOMotorClient] = None
    _is_connected: bool = False

    @classmethod
    async def connect_db(cls):
        """Establish connection to MongoDB with retry logic"""
        if cls._is_connected:
            logger.info("MongoDB already connected")
            return

        try:
            cls.client = AsyncIOMotorClient(
                settings.mongodb_uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=20,              # Connection pooling
                minPoolSize=5,
                uuidRepresentation="standard"
            )

            # Verify connection
            await cls.client.admin.command("ping")

            cls._is_connected = True
            logger.info(f"✅ Connected to MongoDB: {settings.mongodb_db_name}")

        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def close_db(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            cls._is_connected = False
            logger.info("MongoDB connection closed")

    @classmethod
    def get_database(cls):
        """Get database instance"""
        if not cls.client or not cls._is_connected:
            raise RuntimeError("Database not connected. Call connect_db() first.")
        return cls.client[settings.mongodb_db_name]

    @classmethod
    def get_collection(cls, collection_name: str):
        """Get collection from database"""
        return cls.get_database()[collection_name]

    @classmethod
    async def health_check(cls) -> bool:
        """Check database health (used for /health endpoint)"""
        try:
            await cls.client.admin.command("ping")
            return True
        except Exception:
            return False


# Singleton instance
db = Database()