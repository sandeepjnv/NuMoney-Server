from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Member, MemberBalance
from ..schemas.member import MemberCreate, MemberUpdate, MemberResponse, MemberBalanceCreate, MemberBalanceResponse

router = APIRouter(prefix="/members", tags=["members"])


@router.post("", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(
        trip_id=member.trip_id,
        name=member.name
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.patch("/{member_id}", response_model=MemberResponse)
def update_member(member_id: str, member_update: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    member.name = member_update.name
    db.commit()
    db.refresh(member)
    return member


@router.delete("/{member_id}")
def delete_member(member_id: str, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    db.delete(member)
    db.commit()
    return {"success": True}


@router.post("/{member_id}/balance", response_model=MemberBalanceResponse)
def set_member_balance(
    member_id: str,
    balance: MemberBalanceCreate,
    trip_id: str,
    db: Session = Depends(get_db)
):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    existing = db.query(MemberBalance).filter(
        MemberBalance.member_id == member_id,
        MemberBalance.currency == balance.currency
    ).first()

    if existing:
        existing.amount = balance.amount
        existing.fx_rate = balance.fx_rate
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_balance = MemberBalance(
            member_id=member_id,
            trip_id=trip_id,
            currency=balance.currency,
            amount=balance.amount,
            fx_rate=balance.fx_rate
        )
        db.add(db_balance)
        db.commit()
        db.refresh(db_balance)
        return db_balance
