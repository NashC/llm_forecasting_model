from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.models.financial_model import FinancialModel
from app.models.data_source import DataSource
from app.auth.deps import get_current_active_user


def get_financial_model(
    model_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> FinancialModel:
    """
    Get a financial model by ID, check if the current user has access to it
    """
    model = db.query(FinancialModel).filter(FinancialModel.id == model_id).first()
    
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial model not found",
        )
    
    # Check if user owns the model or if the model is public
    if model.owner_id != current_user.id and not model.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this model",
        )
    
    return model


def get_data_source(
    source_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> DataSource:
    """
    Get a data source by ID, check if the current user has access to it
    """
    source = db.query(DataSource).filter(DataSource.id == source_id).first()
    
    if not source:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Data source not found",
        )
    
    # Check if user owns the data source
    if source.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this data source",
        )
    
    return source 