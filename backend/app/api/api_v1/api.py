from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, financial_models, data_sources, chat

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(financial_models.router, prefix="/models", tags=["financial_models"])
api_router.include_router(data_sources.router, prefix="/data-sources", tags=["data_sources"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"]) 