from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routes.deps import get_db
from app.models import Asset
from app.schemas import AssetCreate, AssetOut

router = APIRouter(prefix="/assets", tags=["assets"])


@router.post("", response_model=AssetOut)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(
        name=payload.name,
        type=payload.type,
        max_allowed_uses=payload.max_allowed_uses,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


@router.get("", response_model=list[AssetOut])
def list_assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()