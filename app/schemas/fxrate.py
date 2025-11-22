from pydantic import BaseModel


class FXRateCreate(BaseModel):
    trip_id: str
    currency: str
    rate: float
    date: str


class FXRateResponse(BaseModel):
    id: str
    trip_id: str
    currency: str
    rate: float
    date: str

    class Config:
        from_attributes = True
