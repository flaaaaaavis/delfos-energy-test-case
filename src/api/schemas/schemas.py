from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DataResponse(BaseModel):
    timestamp: datetime
    wind_speed: Optional[float] = None
    power: Optional[float] = None
    ambient_temperature: Optional[float] = None

    class Config:
        from_attributes = True