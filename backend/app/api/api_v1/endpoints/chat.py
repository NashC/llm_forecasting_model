from typing import Any, List, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.auth.deps import get_current_active_user
from app.services.llm_service import get_model_response, generate_forecast_code

router = APIRouter()


@router.post("/message", response_model=Dict)
async def chat_message(
    *,
    message: str = Body(..., embed=True),
    conversation_id: Optional[str] = Body(None, embed=True),
    context: Optional[Dict] = Body(None, embed=True),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Send a message to the LLM and get a response.
    """
    response = await get_model_response(
        user_id=current_user.id,
        message=message,
        conversation_id=conversation_id,
        context=context,
    )
    
    return response


@router.post("/generate-forecast", response_model=Dict)
async def generate_forecast(
    *,
    message: str = Body(..., embed=True),
    model_type: str = Body(..., embed=True),
    historical_data: Optional[Dict] = Body(None, embed=True),
    assumptions: Optional[Dict] = Body(None, embed=True),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Generate a financial forecast model based on the user's specifications.
    """
    code, parameters = await generate_forecast_code(
        user_id=current_user.id,
        message=message,
        model_type=model_type,
        historical_data=historical_data,
        assumptions=assumptions,
    )
    
    return {
        "code": code,
        "parameters": parameters,
        "model_type": model_type,
    } 