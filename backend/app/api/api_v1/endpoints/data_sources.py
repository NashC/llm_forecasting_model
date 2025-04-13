from typing import Any, List, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.user import User
from app.models.data_source import DataSource
from app.models.schemas.data_source import (
    DataSource as DataSourceSchema,
    DataSourceCreate,
    DataSourceUpdate,
)
from app.auth.deps import get_current_active_user
from app.api.deps import get_data_source
from app.services.data_importer import import_data, get_data_preview

router = APIRouter()


@router.get("", response_model=List[DataSourceSchema])
def list_data_sources(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    source_type: Optional[str] = None,
) -> Any:
    """
    Retrieve data sources.
    """
    query = db.query(DataSource).filter(DataSource.owner_id == current_user.id)
    
    if source_type:
        query = query.filter(DataSource.source_type == source_type)
    
    sources = query.offset(skip).limit(limit).all()
    return sources


@router.post("", response_model=DataSourceSchema)
def create_data_source(
    *,
    db: Session = Depends(get_db),
    source_in: DataSourceCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new data source.
    """
    source = DataSource(
        name=source_in.name,
        description=source_in.description,
        source_type=source_in.source_type,
        connection_info=source_in.connection_info,
        schema=source_in.schema,
        is_active=source_in.is_active,
        owner_id=current_user.id,
    )
    
    db.add(source)
    db.commit()
    db.refresh(source)
    
    return source


@router.get("/{source_id}", response_model=DataSourceSchema)
def get_data_source_by_id(
    source: DataSource = Depends(get_data_source),
) -> Any:
    """
    Get a specific data source by id.
    """
    return source


@router.put("/{source_id}", response_model=DataSourceSchema)
def update_data_source(
    *,
    db: Session = Depends(get_db),
    source: DataSource = Depends(get_data_source),
    source_in: DataSourceUpdate,
) -> Any:
    """
    Update a data source.
    """
    data_to_update = source_in.dict(exclude_unset=True)
    for field, value in data_to_update.items():
        setattr(source, field, value)
    
    db.add(source)
    db.commit()
    db.refresh(source)
    
    return source


@router.delete("/{source_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_data_source(
    *,
    db: Session = Depends(get_db),
    source: DataSource = Depends(get_data_source),
) -> Any:
    """
    Delete a data source.
    """
    db.delete(source)
    db.commit()
    return None


@router.post("/upload/file", response_model=Dict)
async def upload_file_data(
    *,
    file: UploadFile = File(...),
    name: str = Form(...),
    source_type: str = Form(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload a file as a data source.
    """
    # Get file contents
    contents = await file.read()
    
    # Process file based on type
    preview, schema = get_data_preview(file.filename, contents, source_type)
    
    # Return preview and schema for frontend to display before saving
    return {
        "name": name,
        "description": description,
        "source_type": source_type,
        "preview": preview,
        "schema": schema,
        "file_name": file.filename,
    }


@router.post("/{source_id}/import", response_model=Dict)
def import_data_from_source(
    *,
    source: DataSource = Depends(get_data_source),
) -> Any:
    """
    Import data from a data source.
    """
    # Import data from source
    data = import_data(source)
    
    return {
        "data": data,
        "rows": len(data),
        "columns": len(data[0]) if data else 0,
    } 