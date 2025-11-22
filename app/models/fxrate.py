from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
import uuid


class FXRate(Base):
    __tablename__ = "fx_rates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id = Column(String, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    currency = Column(String, nullable=False)
    rate = Column(Float, nullable=False)
    date = Column(String, nullable=False)

    trip = relationship("Trip", back_populates="fx_rates")
