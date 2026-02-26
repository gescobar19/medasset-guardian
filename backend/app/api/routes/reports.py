from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.routes.deps import get_db
from app.models import Asset, UsageLog, AssetStatus

router = APIRouter(tags=["reports"])


@router.get("/risk-report/{asset_id}")
def risk_report(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    total_uses = (
        db.query(func.coalesce(func.sum(UsageLog.uses_added), 0))
        .filter(UsageLog.asset_id == asset_id)
        .scalar()
    )
    total_uses = int(total_uses or 0)

    degraded_mode = False

    if asset.max_allowed_uses is None or asset.max_allowed_uses <= 0:
        recommended_status = AssetStatus.NEEDS_INSPECTION
        reason = "max_allowed_uses not set (or <= 0). Defaulting to conservative status."
        degraded_mode = True
    elif total_uses >= asset.max_allowed_uses:
        recommended_status = AssetStatus.RETIRED
        reason = "Total uses reached/exceeded max_allowed_uses."
    else:
        recommended_status = AssetStatus.ACTIVE
        reason = "Total uses within allowed limit."

    # Persist status if changed
    if asset.status != recommended_status:
        asset.status = recommended_status
        db.commit()

    return {
        "asset_id": asset.id,
        "name": asset.name,
        "type": asset.type,
        "max_allowed_uses": asset.max_allowed_uses,
        "total_uses": total_uses,
        "recommended_status": recommended_status.value,
        "degraded_mode": degraded_mode,
        "reason": reason,
    }