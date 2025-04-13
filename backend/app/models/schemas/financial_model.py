from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

from .user import User


class ModelVersionBase(BaseModel):
    version_number: int
    code: str
    parameters: Dict[str, Any]
    description: Optional[str] = None


class ModelVersionCreate(ModelVersionBase):
    pass


class ModelVersionUpdate(BaseModel):
    code: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class ModelVersionInDBBase(ModelVersionBase):
    id: int
    model_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ModelVersion(ModelVersionInDBBase):
    pass


class FinancialModelBase(BaseModel):
    name: str
    description: Optional[str] = None
    model_type: str
    code: str
    parameters: Dict[str, Any]
    is_public: bool = False


class FinancialModelCreate(FinancialModelBase):
    pass


class FinancialModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    model_type: Optional[str] = None
    code: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None
    is_public: Optional[bool] = None


class FinancialModelInDBBase(FinancialModelBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FinancialModel(FinancialModelInDBBase):
    owner: Optional[User] = None
    versions: Optional[List[ModelVersion]] = []


class FinancialModelWithResult(FinancialModel):
    result: Optional[Dict[str, Any]] = None 