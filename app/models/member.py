from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import uuid


class Member(Base):
    __tablename__ = "members"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    avatar = Column(String, nullable=True)

    trip = relationship("Trip", back_populates="members")
    balances = relationship("MemberBalance", back_populates="member", cascade="all, delete-orphan")
    expenses_paid = relationship("Expense", back_populates="paid_by", foreign_keys="Expense.paid_by_id")
    expense_shares = relationship("ExpenseShare", back_populates="member", cascade="all, delete-orphan")


class MemberBalance(Base):
    __tablename__ = "member_balances"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    member_id = Column(String, ForeignKey("members.id", ondelete="CASCADE"), nullable=False)
    trip_id = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    amount = Column(Float, default=0)
    fx_rate = Column(Float, nullable=True)

    member = relationship("Member", back_populates="balances")
