"""
FastAPI server for voice-based patient registration.
Handles REST API endpoints and Vapi.ai webhook integration.
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

from config.database import create_tables, close_database
from config.settings import settings
from routers import patients, vapi

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 50)
    logger.info("🚀 Voice AI Agent Backend Server Starting")
    logger.info(f"📡 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🗄️  Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    
    # Create database tables
    await create_tables()
    logger.info("✅ Database tables ready")
    logger.info("📞 Ready to receive calls and API requests")
    logger.info("=" * 50)
    
    yield
    
    logger.info("Shutting down...")
    await close_database()
    logger.info("✅ Database connections closed")

app = FastAPI(
    title="Voice AI Patient Registration API",
    description="REST API for voice-based patient demographic registration",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router, prefix="/api/patients", tags=["patients"])
app.include_router(vapi.router, prefix="/api/vapi", tags=["vapi"])

@app.get("/")
async def root():
    return {
        "message": "Voice AI Agent - Patient Registration System API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "patients": "/api/patients",
            "vapi_webhook": "/api/vapi/webhook"
        },
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "voice-ai-agent-backend",
        "version": "1.0.0"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc) if settings.ENVIRONMENT == "development" else "An unexpected error occurred",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development"
    )
