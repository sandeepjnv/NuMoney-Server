from pydantic import BaseModel
from typing import List


class MemberLedger(BaseModel):
    member_id: str
    member_name: str
    starting_balance_inr: float
    starting_balance_myr: float
    total_spent: float
    total_share: float
    net_balance: float


class Settlement(BaseModel):
    from_member_id: str
    from_member_name: str
    to_member_id: str
    to_member_name: str
    amount: float
    amount_in_myr: float


class SettlementResponse(BaseModel):
    ledger: List[MemberLedger]
    settlements: List[Settlement]
    current_rate: float
