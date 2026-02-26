from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.routes.deps import get_db
from app.models import Asset, UsageLog
from app.schemas import UsageCreate

router = APIRouter(tags=["usage"])

@router.post("/usage")
def log_usage(payload: UsageCreate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == payload.asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    log = UsageLog(asset_id=payload.asset_id, uses_added=payload.uses_added)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log