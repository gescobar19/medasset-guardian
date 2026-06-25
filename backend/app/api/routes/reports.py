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

    # Determine recommended status
    if asset.max_allowed_uses is None or asset.max_allowed_uses <= 0:
        recommended_status = AssetStatus.NEEDS_INSPECTION
        reason = (
            "max_allowed_uses not set (or <= 0). "
            "Defaulting to conservative status."
        )
        degraded_mode = True

    elif total_uses >= asset.max_allowed_uses:
        recommended_status = AssetStatus.RETIRED
        reason = "Total operating cycles reached/exceeded service life limit."

    else:
        recommended_status = AssetStatus.ACTIVE
        reason = "Equipment remains within expected service life."

    # Persist status changes
    if asset.status != recommended_status:
        asset.status = recommended_status
        db.commit()

    # Health Score + Risk Level
    if degraded_mode:
        health_score = 0
        risk_level = "HIGH"
        remaining_uses = 0

    else:
        usage_ratio = total_uses / asset.max_allowed_uses

        health_score = max(
            0,
            round(100 - (usage_ratio * 100))
        )

        remaining_uses = max(
            0,
            asset.max_allowed_uses - total_uses
        )

        if health_score >= 80:
            risk_level = "LOW"
        elif health_score >= 50:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

    # Recommendation Engine
    if risk_level == "LOW":
        recommendation = (
            "Continue normal operation."
        )

    elif risk_level == "MEDIUM":
        recommendation = (
            "Schedule preventive maintenance."
        )

    else:
        recommendation = (
            "Inspect immediately and consider replacement."
        )

    return {
        "asset_id": asset.id,
        "name": asset.name,
        "type": asset.type,
        "health_score": health_score,
        "risk_level": risk_level,
        "remaining_uses": remaining_uses,
        "max_allowed_uses": asset.max_allowed_uses,
        "total_uses": total_uses,
        "recommended_status": recommended_status.value,
        "reason": reason,
        "recommendation": recommendation,
    }