from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import FXRate
from ..schemas.fxrate import FXRateCreate, FXRateResponse

router = APIRouter(prefix="/fxrates", tags=["fxrates"])


@router.post("", response_model=FXRateResponse)
def set_fx_rate(fx_rate: FXRateCreate, db: Session = Depends(get_db)):
    existing = db.query(FXRate).filter(
        FXRate.trip_id == fx_rate.trip_id,
        FXRate.currency == fx_rate.currency,
        FXRate.date == fx_rate.date
    ).first()

    if existing:
        existing.rate = fx_rate.rate
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_rate = FXRate(
            trip_id=fx_rate.trip_id,
            currency=fx_rate.currency,
            rate=fx_rate.rate,
            date=fx_rate.date
        )
        db.add(db_rate)
        db.commit()
        db.refresh(db_rate)
        return db_rate
