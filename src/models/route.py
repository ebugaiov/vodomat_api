from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from .base import Base

from pydantic import BaseModel


class Route(Base):
    __tablename__ = 'route'

    id = Column(Integer, primary_key=True)
    name = Column(String(16))
    car_number = Column(String(16))
    driver_1 = Column(String(32))
    driver_2 = Column(String(32))

    avtomats = relationship('Avtomat', back_populates='route')
