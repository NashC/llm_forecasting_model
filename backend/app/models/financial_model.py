from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.db.base import Base

class FinancialModel(Base):
    __tablename__ = "financial_models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    model_type = Column(String, index=True)  # revenue, expense, cash flow, etc.
    code = Column(Text)  # Python code for the model
    parameters = Column(JSON)  # Model assumptions and parameters
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    owner = relationship("User", back_populates="models")
    versions = relationship("ModelVersion", back_populates="model")
    
    def __repr__(self):
        return f"FinancialModel(id={self.id}, name={self.name}, type={self.model_type})"


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(Integer, ForeignKey("financial_models.id"))
    version_number = Column(Integer)
    code = Column(Text)  # Python code for this version
    parameters = Column(JSON)  # Model assumptions for this version
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    model = relationship("FinancialModel", back_populates="versions")
    
    def __repr__(self):
        return f"ModelVersion(id={self.id}, model_id={self.model_id}, version={self.version_number})" 