from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from .base import Base
import uuid


class Trip(Base):
    __tablename__ = "trips"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    base_currency = Column(String, default="INR")
    supported_currencies = Column(String, default="INR,MYR")
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    is_deleted = Column(Boolean, default=False)

    members = relationship("Member", back_populates="trip", cascade="all, delete-orphan")
    fx_rates = relationship("FXRate", back_populates="trip", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")
