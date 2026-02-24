from fastapi import FastAPI, Depends, HTTPException
from database import Base, engine, SessionLocal
from models import Base, Asset, Inspection, UsageLog
from sqlalchemy.orm import Session
from schemas import AssetCreate, InspectionCreate, UsageCreate
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/assets")
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)):
    asset = Asset(
        name = payload.name,
        type = payload.type,
        max_allowed_uses = payload.max_allowed_uses,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@app.get("/assets")
def list_assets(db: Session = Depends(get_db)):
    return db.query(Asset).all()

@app.post("/usage")
def log_usage(payload: UsageCreate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == payload.asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    log = UsageLog(asset_id=payload.asset_id, uses_added = payload.uses_added)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

@app.get("/risk-report/{asset_id}")
def risk_report(asset_id: int, db: Session = Depends(get_db)):
    # 1) Asset must exist
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    # 2) Compute total uses (0 if no logs)
    total_uses = (
        db.query(func.coalesce(func.sum(UsageLog.uses_added), 0))
        .filter(UsageLog.asset_id == asset_id)
        .scalar()
    )
    total_uses = int(total_uses)

    # 3) v1 decision logic
    degraded_mode = False

    if asset.max_allowed_uses is None or asset.max_allowed_uses <= 0:
        recommended_status = "NEEDS_INSPECTION"
        reason = "max_allowed_uses not set (or <= 0). Defaulting to conservative status."
        degraded_mode = True
    elif total_uses >= asset.max_allowed_uses:
        recommended_status = "RETIRED"
        reason = "Total uses reached/exceeded max_allowed_uses."
    else:
        recommended_status = "ACTIVE"
        reason = "Total uses within allowed limit."

    # 4) Optional: persist the recommended status
    if asset.status != recommended_status:
        asset.status = recommended_status
        db.commit()

    # 5) Return report
    return {
        "asset_id": asset.id,
        "name": asset.name,
        "type": asset.type,
        "max_allowed_uses": asset.max_allowed_uses,
        "total_uses": total_uses,
        "recommended_status": recommended_status,
        "degraded_mode": degraded_mode,
        "reason": reason,
    }

@app.post("/inspection")
def inspection(payload: InspectionCreate, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == payload.asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    if payload.condition_rating < 1 or payload.condition_rating > 5:
        raise HTTPException(status_code=400, detail="condition_rating must be between 1 and 5")

    inspection = Inspection(
        asset_id=payload.asset_id,
        condition_rating=payload.condition_rating,
        notes=payload.notes
    )
    db.add(inspection)
    db.commit()
    db.refresh(inspection)
    return inspection