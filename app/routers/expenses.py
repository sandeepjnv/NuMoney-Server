from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Expense, ExpenseShare
from ..schemas.expense import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=ExpenseResponse, status_code=201)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    amount_in_base = expense.amount if expense.currency == "INR" else expense.amount * expense.fx_rate

    db_expense = Expense(
        trip_id=expense.trip_id,
        paid_by_id=expense.paid_by_id,
        amount=expense.amount,
        currency=expense.currency,
        description=expense.description,
        category=expense.category,
        date=expense.date,
        split_method=expense.split_method,
        fx_rate=expense.fx_rate,
        amount_in_base=amount_in_base
    )
    db.add(db_expense)
    db.flush()

    for share in expense.shares:
        db_share = ExpenseShare(
            expense_id=db_expense.id,
            member_id=share.member_id,
            amount=share.amount,
            amount_in_base=share.amount_in_base
        )
        db.add(db_share)

    db.commit()
    db.refresh(db_expense)
    return db_expense


@router.delete("/{expense_id}")
def delete_expense(expense_id: str, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()
    return {"success": True}
