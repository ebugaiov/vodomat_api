from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from typing_extensions import Optional

from db.databases import Model


class City(Model):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(32))

    streets: Mapped[list['Street']] = relationship(back_populates='city')

    def __repr__(self):
        return f'City("{self.city}")'


class Street(Model):
    __tablename__ = 'street'

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(String(64))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))

    city: Mapped['City'] = relationship(back_populates='streets')
    avtomats: Mapped[list['Avtomat']] = relationship(back_populates='street')

    @hybrid_property
    def city_name(self):
        return self.city.city

    def __repr__(self):
        return f'Street({self.city_id}, "{self.street}")'


class Route(Model):
    __tablename__ = 'route'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(16))
    car_number: Mapped[str] = mapped_column(String(16))
    driver_1: Mapped[str] = mapped_column(String(32))
    driver_2: Mapped[str] = mapped_column(String(32))

    avtomats: Mapped[list['Avtomat']] = relationship(back_populates='route')

    def __repr__(self):
        return f'Route({self.name}, "{self.car_number}")'


class Avtomat(Model):
    __tablename__ = 'avtomat'

    avtomat_number: Mapped[int] = mapped_column(primary_key=True)
    house: Mapped[str] = mapped_column(String(16))
    latitude: Mapped[Optional[float]]
    longitude: Mapped[Optional[float]]
    search_radius: Mapped[int]
    price: Mapped[int]
    price_for_app: Mapped[int]
    max_sum: Mapped[int]
    size: Mapped[int]
    competitors: Mapped[bool]
    state: Mapped[int]
    payment_app_url: Mapped[Optional[str]]
    rro_id: Mapped[int]
    security_id: Mapped[int] = mapped_column(String(24))
    security_state: Mapped[int]
    route_id: Mapped[int] = mapped_column(ForeignKey('route.id'))
    street_id: Mapped[int] = mapped_column(ForeignKey('street.id'))

    route: Mapped['Route'] = relationship(back_populates='avtomats')
    street: Mapped['Street'] = relationship(back_populates='avtomats')
    status: Mapped['Status'] = relationship(back_populates='avtomat')
    statistic: Mapped['Statistic'] = relationship(back_populates='avtomat')

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

    @hybrid_property
    def address(self):
        return f'{self.city_name}, {self.street_name}, {self.house}'

    def __repr__(self):
        return f'Avtomat({self.avtomat_number}, "{self.address}")'


class BaseStatusLine(Model):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    avtomat_number: Mapped[int] = mapped_column(ForeignKey('avtomat.avtomat_number'))
    time: Mapped[datetime]
    water: Mapped[int]
    money: Mapped[int]
    money_app: Mapped[int]
    price: Mapped[int]
    grn: Mapped[int]
    kop: Mapped[int]
    bill_not_work: Mapped[int]
    coin_not_work: Mapped[int]
    bill_not_work_money: Mapped[int]
    coin_not_work_money: Mapped[int]
    time_to_block: Mapped[int]
    low_water_balance: Mapped[bool]
    error_volt: Mapped[bool]
    error_bill: Mapped[bool]
    error_counter: Mapped[bool]
    error_register: Mapped[bool]
    cashbox: Mapped[bool]
    gsm: Mapped[int]
    event: Mapped[int]

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


class Status(BaseStatusLine):
    __tablename__ = 'status'

    avtomat: Mapped[Avtomat] = relationship(back_populates='status')

    @hybrid_property
    def house(self):
        return self.avtomat.house

    @hybrid_property
    def street(self):
        return self.avtomat.street_name

    @hybrid_property
    def city(self):
        return self.avtomat.city_name

    @hybrid_property
    def route_name(self):
        return self.avtomat.route_name

    @hybrid_property
    def route_car_number(self):
        return self.avtomat.route_car_number

    @hybrid_property
    def size(self):
        return self.avtomat.size

    @hybrid_property
    def state(self):
        return self.avtomat.state


class Statistic(BaseStatusLine):
    __tablename__ = 'statistic'

    avtomat: Mapped[Avtomat] = relationship(back_populates='statistic')
