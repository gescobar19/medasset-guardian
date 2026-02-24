from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    max_allowed_uses = Column(Integer, nullable=False)
    status = Column(String, default="ACTIVE")
    date_added = Column(DateTime, default=datetime.utcnow)
    inspections = relationship("Inspection", back_populates="asset")

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    uses_added = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    condition_rating = Column(Integer, nullable=False)
    notes = Column(String, nullable=True) # makes notes optional
    date = Column(DateTime, default=datetime.utcnow)
    asset = relationship("Asset", back_populates="inspections")