from sqlalchemy import Column
from sqlalchemy import Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from .base import Base


class Avtomat(Base):
    __tablename__ = 'avtomat'

    avtomat_number = Column(Integer, primary_key=True)
    route_id = Column(Integer, ForeignKey('route.id'))
    street_id = Column(Integer, ForeignKey('street.id'))
    house = Column(String(16))
    latitude = Column(Float)
    longitude = Column(Float)
    search_radius = Column(Integer)
    price = Column(Integer)
    price_for_app = Column(Integer)
    payment_app_url = Column(String(64))
    payment_gateway_name = Column(String(64))
    payment_gateway_url = Column(String(64))
    max_sum = Column(Integer)
    size = Column(Integer)
    competitors = Column(Boolean)
    state = Column(TINYINT)
    rro_id = Column(Integer)
    security_id = Column(String(24))
    security_state = Column(TINYINT)

    route = relationship('Route', back_populates='avtomats')
    street = relationship('Street', back_populates='avtomats')
    status = relationship('Status', back_populates='avtomat')

    @hybrid_property
    def route_name(self):
        return self.route.name if self.route else None

    @hybrid_property
    def route_car_number(self):
        return self.route.car_number if self.route else None

    @hybrid_property
    def street_name(self):
        return self.street.street if self.street else None

    @hybrid_property
    def city_name(self):
        return self.street.city.city if self.street.city else None
