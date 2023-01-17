from sqlalchemy import Column
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Street(Base):
    __tablename__ = 'street'

    id = Column(Integer, primary_key=True)
    street = Column(String(64))
    city_id = Column(Integer, ForeignKey('city.id'))

    city = relationship('City', back_populates='streets')
    avtomats = relationship('Avtomat', back_populates='street')

    @property
    def city_name(self):
        return self.city.city
