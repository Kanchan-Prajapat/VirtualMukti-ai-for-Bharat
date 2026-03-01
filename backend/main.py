"""
FastAPI main application entry point
Production-ready configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from .config import settings
from .database import db
from .repositories.user_repository import UserRepository
from .repositories.user_activity_repository import UserActivityRepository

# -------------------------
# Logging Configuration
# -------------------------
logging.basicConfig(
    level=logging.INFO if settings.app_env == "production" else logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


# -------------------------
# Lifespan Events
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""

    logger.info("🚀 Starting VirtualMukti backend...")

    # Connect to MongoDB
    await db.connect_db()

    # Create database indexes
    logger.info("📦 Creating database indexes...")
    await UserRepository.create_indexes()
    await UserActivityRepository.create_indexes()

    logger.info("✅ Backend started successfully")
    yield

    # Shutdown
    logger.info("🛑 Shutting down backend...")
    await db.close_db()
    logger.info("✅ Backend shut down cleanly")


# -------------------------
# FastAPI App Instance
# -------------------------
app = FastAPI(
    title=settings.app_name,
    description="AI-Powered Addiction Recovery Platform",
    version="1.0.0",
    lifespan=lifespan,
)


# -------------------------
# CORS Configuration
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list or ["*"]
    if settings.app_env == "development"
    else settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Global Exception Handler
# -------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# -------------------------
# Basic Routes
# -------------------------
@app.get("/")
async def root():
    return {
        "message": "VirtualMukti API",
        "version": "1.0.0",
        "environment": settings.app_env,
        "status": "running",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
    }


# -------------------------
# Router Registration
# -------------------------
from .api.auth import router as auth_router
from .api.ml import router as ml_router
from .api.chatbot import router as chatbot_router
from .api.helplines import router as helplines_router
from .api.stories import router as stories_router
from .api.motivation import router as motivation_router
from .api.rehab import router as rehab_router

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(ml_router, prefix="/api/ml", tags=["Machine Learning"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(helplines_router, prefix="/api/helplines", tags=["Helplines"])
app.include_router(stories_router, prefix="/api/stories", tags=["Stories"])
app.include_router(motivation_router, prefix="/api/motivation", tags=["Motivation"])
app.include_router(rehab_router, prefix="/api/rehab", tags=["Rehab"])


# -------------------------
# Local Development Run
# -------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development",
    )