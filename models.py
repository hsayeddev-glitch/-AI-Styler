from pydantic import BaseModel
from typing import List, Optional

class ClothingItem(BaseModel):
    id: int
    filename: str
    category: str
    color: str
    uploaded_at: Optional[str] = None

class OutfitResult(BaseModel):
    style: str
    items: List[ClothingItem]
    missing_categories: List[str]
    complete: bool

class UsageLimits(BaseModel):
    user_id: str
    date: str
    outfits_generated: int
    clothes_uploaded: int
