from pydantic import BaseModel
from typing import Optional, List


class MemberBalanceCreate(BaseModel):
    currency: str
    amount: float
    fx_rate: Optional[float] = None


class MemberBalanceResponse(BaseModel):
    id: str
    member_id: str
    trip_id: str
    currency: str
    amount: float
    fx_rate: Optional[float]

    class Config:
        from_attributes = True


class MemberCreate(BaseModel):
    trip_id: str
    name: str


class MemberUpdate(BaseModel):
    name: str


class MemberResponse(BaseModel):
    id: str
    trip_id: str
    name: str
    avatar: Optional[str]
    balances: List[MemberBalanceResponse] = []

    class Config:
        from_attributes = True
