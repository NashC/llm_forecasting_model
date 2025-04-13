from typing import Any, List, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Body, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.models.financial_model import FinancialModel, ModelVersion
from app.models.schemas.financial_model import (
    FinancialModel as FinancialModelSchema,
    FinancialModelCreate,
    FinancialModelUpdate,
    FinancialModelWithResult,
    ModelVersion as ModelVersionSchema,
    ModelVersionCreate,
)
from app.auth.deps import get_current_active_user
from app.api.deps import get_financial_model
from app.services.model_runner import run_model, generate_model_code

router = APIRouter()


@router.get("", response_model=List[FinancialModelSchema])
def list_financial_models(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    model_type: Optional[str] = None,
) -> Any:
    """
    Retrieve financial models.
    """
    query = db.query(FinancialModel)
    query = query.filter(
        (FinancialModel.owner_id == current_user.id) | (FinancialModel.is_public == True)
    )
    
    if model_type:
        query = query.filter(FinancialModel.model_type == model_type)
    
    models = query.offset(skip).limit(limit).all()
    return models


@router.post("", response_model=FinancialModelSchema)
def create_financial_model(
    *,
    db: Session = Depends(get_db),
    model_in: FinancialModelCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new financial model.
    """
    model = FinancialModel(
        name=model_in.name,
        description=model_in.description,
        model_type=model_in.model_type,
        code=model_in.code,
        parameters=model_in.parameters,
        is_public=model_in.is_public,
        owner_id=current_user.id,
    )
    
    db.add(model)
    db.commit()
    db.refresh(model)
    
    # Create initial version
    version = ModelVersion(
        model_id=model.id,
        version_number=1,
        code=model.code,
        parameters=model.parameters,
        description=f"Initial version of {model.name}",
    )
    
    db.add(version)
    db.commit()
    
    return model


@router.get("/{model_id}", response_model=FinancialModelSchema)
def get_financial_model_by_id(
    model: FinancialModel = Depends(get_financial_model),
) -> Any:
    """
    Get a specific financial model by id.
    """
    return model


@router.put("/{model_id}", response_model=FinancialModelSchema)
def update_financial_model(
    *,
    db: Session = Depends(get_db),
    model: FinancialModel = Depends(get_financial_model),
    model_in: FinancialModelUpdate,
) -> Any:
    """
    Update a financial model.
    """
    # Create a new version if code or parameters have changed
    create_new_version = False
    version_number = 1
    
    if len(model.versions) > 0:
        version_number = max([v.version_number for v in model.versions]) + 1
    
    if (model_in.code is not None and model_in.code != model.code) or (
        model_in.parameters is not None and model_in.parameters != model.parameters
    ):
        create_new_version = True
    
    # Update model attributes
    data_to_update = model_in.dict(exclude_unset=True)
    for field, value in data_to_update.items():
        setattr(model, field, value)
    
    db.add(model)
    db.commit()
    db.refresh(model)
    
    # Create new version if needed
    if create_new_version:
        version = ModelVersion(
            model_id=model.id,
            version_number=version_number,
            code=model.code,
            parameters=model.parameters,
            description=f"Version {version_number} of {model.name}",
        )
        
        db.add(version)
        db.commit()
    
    return model


@router.delete("/{model_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_financial_model(
    *,
    db: Session = Depends(get_db),
    model: FinancialModel = Depends(get_financial_model),
) -> Any:
    """
    Delete a financial model.
    """
    db.delete(model)
    db.commit()
    return None


@router.post("/{model_id}/run", response_model=FinancialModelWithResult)
def run_financial_model(
    *,
    model: FinancialModel = Depends(get_financial_model),
    parameters: Optional[Dict] = Body(None),
) -> Any:
    """
    Run a financial model with provided parameters.
    """
    model_params = model.parameters
    
    # Override with provided parameters if any
    if parameters:
        model_params.update(parameters)
    
    # Run the model
    result = run_model(model.code, model_params)
    
    # Return model with results
    return {**model.__dict__, "result": result}


@router.get("/{model_id}/versions", response_model=List[ModelVersionSchema])
def list_model_versions(
    *,
    model: FinancialModel = Depends(get_financial_model),
) -> Any:
    """
    List all versions of a financial model.
    """
    return model.versions


@router.get("/{model_id}/versions/{version_number}", response_model=ModelVersionSchema)
def get_model_version(
    *,
    db: Session = Depends(get_db),
    model: FinancialModel = Depends(get_financial_model),
    version_number: int,
) -> Any:
    """
    Get a specific version of a financial model.
    """
    version = db.query(ModelVersion).filter(
        ModelVersion.model_id == model.id,
        ModelVersion.version_number == version_number,
    ).first()
    
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Model version not found",
        )
    
    return version


@router.post("/generate", response_model=Dict)
def generate_model(
    *,
    current_user: User = Depends(get_current_active_user),
    model_type: str = Query(..., description="Type of financial model to generate"),
    prompt: str = Body(..., description="Description of the model to generate"),
    parameters: Optional[Dict] = Body(None, description="Initial parameters for the model"),
) -> Any:
    """
    Generate a financial model using AI.
    """
    # Generate model code using AI
    code = generate_model_code(model_type, prompt, parameters)
    
    return {
        "code": code,
        "model_type": model_type,
        "parameters": parameters or {},
    } 