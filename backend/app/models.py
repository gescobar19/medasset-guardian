import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.database import Base


class AssetStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    RETIRED = "RETIRED"
    NEEDS_INSPECTION = "NEEDS_INSPECTION"


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    max_allowed_uses = Column(Integer, nullable=False)

    status = Column(
        Enum(AssetStatus, name="asset_status"),
        nullable=False,
        default=AssetStatus.ACTIVE,
        server_default=AssetStatus.ACTIVE.value,
    )

    date_added = Column(DateTime, default=datetime.utcnow)

    inspections = relationship(
        "Inspection",
        back_populates="asset"
    )

    usage_logs = relationship(
        "UsageLog",
        back_populates="asset"
    )

    maintenance_logs = relationship(
        "MaintenanceLog",
        back_populates="asset"
    )
    


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    uses_added = Column(Integer, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    asset = relationship("Asset", back_populates="usage_logs")


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    condition_rating = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

    asset = relationship("Asset", back_populates="inspections")

class MaintenanceLog(Base):
    __tablename__ = "maintenance_logs"

    id = Column(Integer, primary_key=True, index=True)

    asset_id = Column(
        Integer,
        ForeignKey("assets.id"),
        nullable=False
    )

    technician = Column(
        String,
        nullable=False
    )

    notes = Column(
        String,
        nullable=True
    )

    date = Column(
        DateTime,
        default=datetime.utcnow
    )

    asset = relationship(
        "Asset",
        back_populates="maintenance_logs"
    )
