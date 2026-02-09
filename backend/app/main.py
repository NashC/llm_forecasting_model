import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db.base import Base, engine, get_db
from app.models.user import User
from app.auth.jwt import get_password_hash

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="LLM-powered financial forecasting API",
    version="0.1.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")


# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}


# Startup event to create superuser if needed
@app.on_event("startup")
def create_superuser():
    try:
        db = next(get_db())
        # Check if superuser exists
        superuser = db.query(User).filter(User.is_superuser == True).first()
        if not superuser:
            logger.info("Creating default superuser")
            superuser = User(
                email=settings.SUPERUSER_EMAIL,
                username=settings.SUPERUSER_USERNAME,
                full_name="Admin User",
                hashed_password=get_password_hash(settings.SUPERUSER_PASSWORD),
                is_active=True,
                is_superuser=True,
            )
            db.add(superuser)
            db.commit()
            logger.info("Default superuser created")
    except Exception as e:
        logger.error(f"Error creating default superuser: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.ENV == "development",
    ) 