from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.routes.deps import get_db
from app.models import Asset, Inspection
from app.schemas import InspectionCreate

router = APIRouter(tags=["inspections"])


@router.post("/inspection")
def create_inspection(payload: InspectionCreate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == payload.asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    if payload.condition_rating < 1 or payload.condition_rating > 5:
        raise HTTPException(status_code=400, detail="condition_rating must be between 1 and 5")

    inspection = Inspection(
        asset_id=payload.asset_id,
        condition_rating=payload.condition_rating,
        notes=payload.notes,
    )
    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    return inspection