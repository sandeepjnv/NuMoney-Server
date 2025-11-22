from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import Trip, Member, FXRate, Expense, ExpenseShare
from ..schemas.trip import TripCreate, TripUpdate, TripResponse, TripDetailResponse
from ..schemas.settlement import SettlementResponse, MemberLedger, Settlement

router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("", response_model=List[TripResponse])
def get_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).filter(Trip.is_deleted == False).order_by(Trip.created_at.desc()).all()
    return trips


@router.post("", response_model=TripResponse, status_code=201)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    db_trip = Trip(
        name=trip.name,
        start_date=trip.start_date,
        end_date=trip.end_date
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


@router.get("/{trip_id}", response_model=TripDetailResponse)
def get_trip(trip_id: str, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.patch("/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: str, trip_update: TripUpdate, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip_update.name is not None:
        trip.name = trip_update.name
    if trip_update.start_date is not None:
        trip.start_date = trip_update.start_date
    if trip_update.end_date is not None:
        trip.end_date = trip_update.end_date

    db.commit()
    db.refresh(trip)
    return trip


@router.delete("/{trip_id}")
def delete_trip(trip_id: str, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    trip.is_deleted = True
    db.commit()
    return {"success": True}


@router.get("/{trip_id}/settlement", response_model=SettlementResponse)
def get_settlement(trip_id: str, db: Session = Depends(get_db)):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Get current MYR rate
    fx_rates = db.query(FXRate).filter(
        FXRate.trip_id == trip_id,
        FXRate.currency == "MYR"
    ).order_by(FXRate.date.desc()).all()
    current_rate = fx_rates[0].rate if fx_rates else 19.0

    # Calculate ledger
    members = db.query(Member).filter(Member.trip_id == trip_id).all()
    expenses = db.query(Expense).filter(Expense.trip_id == trip_id).all()

    ledger_data = []
    for member in members:
        inr_balance = next((b for b in member.balances if b.currency == "INR"), None)
        myr_balance = next((b for b in member.balances if b.currency == "MYR"), None)

        starting_inr = inr_balance.amount if inr_balance else 0
        starting_myr = myr_balance.amount if myr_balance else 0
        myr_rate = myr_balance.fx_rate if myr_balance and myr_balance.fx_rate else current_rate
        starting_total = starting_inr + starting_myr * myr_rate

        total_spent = sum(e.amount_in_base for e in expenses if e.paid_by_id == member.id)
        total_share = sum(
            s.amount_in_base
            for e in expenses
            for s in e.shares
            if s.member_id == member.id
        )
        net_balance = starting_total + total_spent - total_share

        ledger_data.append(MemberLedger(
            member_id=member.id,
            member_name=member.name,
            starting_balance_inr=starting_inr,
            starting_balance_myr=starting_myr,
            total_spent=total_spent,
            total_share=total_share,
            net_balance=net_balance
        ))

    # Calculate settlements using greedy algorithm
    debtors = [l for l in ledger_data if l.net_balance < 0]
    creditors = [l for l in ledger_data if l.net_balance > 0]

    debtors.sort(key=lambda x: x.net_balance)
    creditors.sort(key=lambda x: -x.net_balance)

    settlements = []
    debtor_balances = {d.member_id: d.net_balance for d in debtors}
    creditor_balances = {c.member_id: c.net_balance for c in creditors}

    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor = debtors[i]
        creditor = creditors[j]

        debt_amount = abs(debtor_balances[debtor.member_id])
        credit_amount = creditor_balances[creditor.member_id]
        amount = min(debt_amount, credit_amount)

        if amount > 0.01:
            settlements.append(Settlement(
                from_member_id=debtor.member_id,
                from_member_name=debtor.member_name,
                to_member_id=creditor.member_id,
                to_member_name=creditor.member_name,
                amount=round(amount, 2),
                amount_in_myr=round(amount / current_rate, 2)
            ))

        debtor_balances[debtor.member_id] += amount
        creditor_balances[creditor.member_id] -= amount

        if abs(debtor_balances[debtor.member_id]) < 0.01:
            i += 1
        if creditor_balances[creditor.member_id] < 0.01:
            j += 1

    return SettlementResponse(
        ledger=ledger_data,
        settlements=settlements,
        current_rate=current_rate
    )
