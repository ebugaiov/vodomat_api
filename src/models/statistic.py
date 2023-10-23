from typing import Optional

from sqlalchemy import Column
from sqlalchemy import Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Base


class Statistic(Base):
    __tablename__ = 'statistic'

    id = Column(Integer, primary_key=True)
    avtomat_number = Column('avtomat_number', Integer(), ForeignKey('avtomat.avtomat_number'))
    time = Column(DateTime)
    water = Column(Integer)
    money = Column(Integer)
    price = Column(Integer)
    grn = Column(Integer)
    kop = Column(Integer)
    money_app = Column(Integer)
    bill_not_work = Column(Integer)
    coin_not_work = Column(Integer)
    bill_not_work_money = Column(Integer)
    coin_not_work_money = Column(Integer)
    time_to_block = Column(Integer)
    low_water_balance = Column(Boolean)
    error_volt = Column(Boolean)
    error_bill = Column(Boolean)
    error_counter = Column(Boolean)
    error_register = Column(Boolean)
    cashbox = Column(Boolean)
    gsm = Column(Integer)
    event = Column(Integer)

    avtomat = relationship('Avtomat', back_populates='statistic')

    @hybrid_property
    def bill_not_work_hours(self) -> int:
        return (self.bill_not_work or 0) // 3600

    @hybrid_property
    def coin_not_work_hours(self) -> int:
        return (self.coin_not_work or 0) // 3600

    @hybrid_property
    def bill_not_work_coins(self) -> float:
        return (self.bill_not_work_money or 0) * 50 / 100

    @hybrid_property
    def coin_not_work_bills(self) -> int:
        return self.coin_not_work_money or 0

    @hybrid_property
    def house(self) -> Optional[str]:
        return self.avtomat.house

    @hybrid_property
    def street(self) -> Optional[str]:
        return self.avtomat.street_name

    @hybrid_property
    def city(self) -> Optional[str]:
        return self.avtomat.city_name

    @hybrid_property
    def route_name(self) -> Optional[str]:
        return self.avtomat.route_name

    @hybrid_property
    def route_car_number(self) -> Optional[str]:
        return self.avtomat.route_car_number
