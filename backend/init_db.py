"""Database initialization script - creates indexes and collections"""

import asyncio
import logging
from database import db
from repositories.user_repository import UserRepository
from repositories.user_activity_repository import UserActivityRepository
from repositories.relapse_prediction_repository import RelapseRiskRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_database():
    """Initialize database with indexes"""
    try:
        # Connect to database
        await db.connect_db()
        logger.info("Connected to MongoDB")
        
        # Create indexes for all collections
        logger.info("Creating indexes...")
        
        await UserRepository.create_indexes()
        await UserActivityRepository.create_indexes()
        await RelapseRiskRepository.create_indexes()
        
        logger.info("Database initialization complete!")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        await db.close_db()


if __name__ == "__main__":
    asyncio.run(init_database())
