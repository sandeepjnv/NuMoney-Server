from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ExpenseShareCreate(BaseModel):
    member_id: str
    amount: float
    amount_in_base: float


class ExpenseShareResponse(BaseModel):
    id: str
    expense_id: str
    member_id: str
    amount: float
    amount_in_base: float

    class Config:
        from_attributes = True


class ExpenseCreate(BaseModel):
    trip_id: str
    paid_by_id: str
    amount: float
    currency: str
    description: str
    category: Optional[str] = None
    date: str
    split_method: str
    fx_rate: float
    shares: List[ExpenseShareCreate]


class ExpenseResponse(BaseModel):
    id: str
    trip_id: str
    paid_by_id: str
    amount: float
    currency: str
    description: str
    category: Optional[str]
    date: str
    split_method: str
    fx_rate: float
    amount_in_base: float
    created_at: datetime
    shares: List[ExpenseShareResponse] = []

    class Config:
        from_attributes = True
