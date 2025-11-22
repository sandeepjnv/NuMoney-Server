from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .member import MemberResponse
from .fxrate import FXRateResponse
from .expense import ExpenseResponse


class TripCreate(BaseModel):
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TripUpdate(BaseModel):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class TripResponse(BaseModel):
    id: str
    name: str
    base_currency: str
    supported_currencies: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    created_at: datetime
    is_deleted: bool

    class Config:
        from_attributes = True


class TripDetailResponse(TripResponse):
    members: List[MemberResponse] = []
    fx_rates: List[FXRateResponse] = []
    expenses: List[ExpenseResponse] = []

    class Config:
        from_attributes = True
