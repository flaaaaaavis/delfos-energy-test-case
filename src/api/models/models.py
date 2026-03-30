from sqlalchemy import Column, DateTime, Float
from src.api.core.database import Base


class Data(Base):
    __tablename__ = "data"

    timestamp = Column(DateTime, primary_key=True, index=True)
    wind_speed = Column(Float)
    power = Column(Float)
    ambient_temperature = Column(Float)