from backend.app.database import SessionLocal
from backend.app.models import Asset, UsageLog, Inspection
from datetime import datetime

def seed():
    db = SessionLocal()

    db.query(Inspection).delete()
    db.query(UsageLog).delete()
    db.query(Asset).delete()
    db.commit()

    # Create assets
    rope = Asset(name="Mammut 9.8mm Rope", type="rope", max_allowed_uses=100, status="ACTIVE")
    harness = Asset(name="Black Diamond Harness", type="harness", max_allowed_uses=200, status="ACTIVE")
    carabiner = Asset(name="Petzl Carabiner", type="carabiner", max_allowed_uses=500, status="ACTIVE")

    db.add_all([rope, harness, carabiner])
    db.commit()

    # Add usage logs
    db.add_all([
        UsageLog(asset_id=rope.id, uses_added=10, date=datetime.utcnow()),
        UsageLog(asset_id=rope.id, uses_added=5, date=datetime.utcnow()),
        UsageLog(asset_id=harness.id, uses_added=30, date=datetime.utcnow()),
    ])
    db.commit()

    db.add_all([
        Inspection(asset_id=rope.id, condition_rating=4, notes="Minor fuzzing", date=datetime.utcnow()),
        Inspection(asset_id=harness.id, condition_rating=3, notes="Slight wear", date=datetime.utcnow()),
        Inspection(asset_id=carabiner.id, condition_rating=5, notes="Excellent condition", date=datetime.utcnow()),
    ])
    db.commit()

    db.close()
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed()