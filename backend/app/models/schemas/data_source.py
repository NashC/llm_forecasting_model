from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

from .user import User


class DataSourceBase(BaseModel):
    name: str
    description: Optional[str] = None
    source_type: str
    connection_info: Dict[str, Any]
    schema: Optional[Dict[str, Any]] = None
    is_active: bool = True


class DataSourceCreate(DataSourceBase):
    pass


class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    source_type: Optional[str] = None
    connection_info: Optional[Dict[str, Any]] = None
    schema: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None


class DataSourceInDBBase(DataSourceBase):
    id: int
    owner_id: int
    last_sync: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DataSource(DataSourceInDBBase):
    owner: Optional[User] = None 