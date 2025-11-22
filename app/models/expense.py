from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from .base import Base
import uuid


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    paid_by_id = Column(String, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=True)
    date = Column(String, nullable=False)
    split_method = Column(String, nullable=False)
    fx_rate = Column(Float, nullable=False)
    amount_in_base = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    trip = relationship("Trip", back_populates="expenses")
    paid_by = relationship("Member", back_populates="expenses_paid", foreign_keys=[paid_by_id])
    shares = relationship("ExpenseShare", back_populates="expense", cascade="all, delete-orphan")


class ExpenseShare(Base):
    __tablename__ = "expense_shares"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String, ForeignKey("expenses.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(String, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    amount_in_base = Column(Float, nullable=False)

    expense = relationship("Expense", back_populates="shares")
    member = relationship("Member", back_populates="expense_shares")
