from sqlalchemy import Column
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    city = Column(String(32))

    streets = relationship('Street', back_populates='city')
