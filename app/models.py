from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # 'user' or 'admin'

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)

    forecasts = relationship("Forecast", back_populates="location")

class Forecast(Base):
    __tablename__ = "forecasts"
    id = Column(Integer, primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id"))
    date = Column(String)
    temperature = Column(String)

    location = relationship("Location", back_populates="forecasts")
