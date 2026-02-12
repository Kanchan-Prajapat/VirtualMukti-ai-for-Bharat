"""Relapse Risk Prediction repository for database operations"""

from typing import Optional, List
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import IndexModel, ASCENDING, DESCENDING

from ..database import db
from ..models.relapse_prediction import (
    RelapseRiskPrediction,
    RiskFactor,
)
import logging

logger = logging.getLogger(__name__)


class RelapseRiskRepository:
    """Repository for RelapseRiskPrediction collection operations"""

    COLLECTION_NAME = "relapse_predictions"

    @classmethod
    def get_collection(cls) -> AsyncIOMotorCollection:
        return db.get_collection(cls.COLLECTION_NAME)

    @classmethod
    async def create_indexes(cls):
        collection = cls.get_collection()

        indexes = [
            IndexModel([("user_id", ASCENDING), ("prediction_date", DESCENDING)]),
            IndexModel([("user_id", ASCENDING)]),
            IndexModel([("prediction_date", DESCENDING)]),
            IndexModel([("risk_score", DESCENDING)]),
            IndexModel([("created_at", DESCENDING)]),
        ]

        await collection.create_indexes(indexes)
        logger.info(f"Created indexes for {cls.COLLECTION_NAME}")

    @classmethod
    async def create(cls, prediction: RelapseRiskPrediction) -> RelapseRiskPrediction:
        collection = cls.get_collection()

        prediction_doc = prediction.model_dump()
        prediction_doc["top_risk_factors"] = [
            factor.model_dump() for factor in prediction.top_risk_factors
        ]

        await collection.insert_one(prediction_doc)
        return prediction

    @classmethod
    async def get_latest(cls, user_id: str) -> Optional[RelapseRiskPrediction]:
        collection = cls.get_collection()

        doc = await collection.find_one(
            {"user_id": user_id},
            sort=[("prediction_date", DESCENDING)]
        )

        if not doc:
            return None

        doc["top_risk_factors"] = [
            RiskFactor(**factor) for factor in doc["top_risk_factors"]
        ]

        return RelapseRiskPrediction(**doc)

    @classmethod
    async def get_by_date(cls, user_id: str, prediction_date: datetime) -> Optional[RelapseRiskPrediction]:
        collection = cls.get_collection()

        start = prediction_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        doc = await collection.find_one({
            "user_id": user_id,
            "prediction_date": {"$gte": start, "$lt": end}
        })

        if not doc:
            return None

        doc["top_risk_factors"] = [
            RiskFactor(**factor) for factor in doc["top_risk_factors"]
        ]

        return RelapseRiskPrediction(**doc)

    @classmethod
    async def get_recent(cls, user_id: str, days: int = 30) -> List[RelapseRiskPrediction]:
        collection = cls.get_collection()
        start_date = datetime.utcnow() - timedelta(days=days)

        cursor = collection.find(
            {"user_id": user_id, "prediction_date": {"$gte": start_date}}
        ).sort("prediction_date", DESCENDING)

        results = []
        async for doc in cursor:
            doc["top_risk_factors"] = [
                RiskFactor(**factor) for factor in doc["top_risk_factors"]
            ]
            results.append(RelapseRiskPrediction(**doc))

        return results

    @classmethod
    async def get_high_risk_users(cls, threshold: float = 70.0, hours: int = 24) -> List[str]:
        collection = cls.get_collection()
        cutoff = datetime.utcnow() - timedelta(hours=hours)

        cursor = collection.find({
            "risk_score": {"$gte": threshold},
            "prediction_date": {"$gte": cutoff}
        })

        return list({doc["user_id"] async for doc in cursor})

    @classmethod
    async def delete_user_predictions(cls, user_id: str) -> int:
        collection = cls.get_collection()
        result = await collection.delete_many({"user_id": user_id})
        return result.deleted_count
