from typing import Optional
from pydantic import BaseModel

class AssetCreate(BaseModel):
    name: str
    type: str
    max_allowed_uses: int

# allows returning SQLAlchemy objects

class AssetOut(BaseModel):
    id: int
    name: str
    type: str
    max_allowed_uses: int
    status: str

    class Config:
        orm_mode = True

class UsageCreate(BaseModel):
    asset_id: int
    uses_added: int

class InspectionCreate(BaseModel):
    asset_id: int
    condition_rating: int
    notes: Optional[str] = None
    