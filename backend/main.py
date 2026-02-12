"""FastAPI main application entry point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from .config import settings
from .database import db
#from .firebase_init import firebase_service
from .repositories.user_repository import UserRepository
from .repositories.user_activity_repository import UserActivityRepository
# from .repositories.relapse_prediction_repository import RelapseRiskRepository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting VirtualMukti backend...")
    await db.connect_db()
    # firebase_service.initialize()
    
    # Create database indexes
    logger.info("Creating database indexes...")
    await UserRepository.create_indexes()
    await UserActivityRepository.create_indexes()
    # await RelapseRiskRepository.create_indexes()
    
    logger.info("VirtualMukti backend started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down VirtualMukti backend...")
    await db.close_db()
    logger.info("VirtualMukti backend shut down successfully")


# Create FastAPI application
app = FastAPI(
    title="VirtualMukti API",
    description="AI-Powered Addiction Recovery Platform for Indian Users",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "VirtualMukti API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "firebase": "initialized"
    }


# Import and include routers
from .api.auth import router as auth_router
from .api.ml import router as ml_router
from .api.chatbot import router as chatbot_router

app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(ml_router, prefix="/api/ml", tags=["Machine Learning"])
app.include_router(chatbot_router, prefix="/api/chatbot", tags=["Chatbot"])

# Additional routers (will be added in later tasks)
# from .api.recovery import router as recovery_router
# from .api.sos import router as sos_router
# from .api.nmk import router as nmk_router

# app.include_router(recovery_router, prefix="/api/recovery", tags=["Recovery"])
# app.include_router(sos_router, prefix="/api/sos", tags=["SOS"])
# app.include_router(nmk_router, prefix="/api/nmk", tags=["NMK Lookup"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development"
    )
