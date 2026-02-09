import os
from typing import List, Union
from pydantic import BaseModel, field_validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    APP_NAME: str = os.getenv("APP_NAME", "LLM Financial Forecasting")
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    PORT: int = int(os.getenv("PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")

    # Database configuration
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/forecasting_db")
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017/forecasting_db")

    # OpenAI configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")

    # JWT configuration
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "jwt_secret")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # Superuser configuration
    SUPERUSER_EMAIL: str = os.getenv("SUPERUSER_EMAIL", "admin@example.com")
    SUPERUSER_USERNAME: str = os.getenv("SUPERUSER_USERNAME", "admin")
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD", "changeme")

    # CORS configuration
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")

    @field_validator("OPENAI_API_KEY")
    def validate_openai_api_key(cls, v):
        if not v and os.getenv("ENV") != "test":
            print("Warning: OPENAI_API_KEY is not set!")
        return v

settings = Settings() 