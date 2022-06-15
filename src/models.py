from sqlalchemy import Table, Column
from sqlalchemy import Integer, Float, String, Boolean, DateTime, ForeignKey
from db.database import database_metadata
from sqlalchemy.dialects.mysql import TINYINT


city = Table(
    'city', database_metadata,

    Column('id', Integer, primary_key=True),
    Column('city', String(32)),
)

street = Table(
    'street', database_metadata,

    Column('id', Integer, primary_key=True),
    Column('street', String(64)),
    Column('city_id', Integer, ForeignKey('city.id', ondelete='SET NULL')),
)

route = Table(
    'route', database_metadata,

    Column('id', Integer, primary_key=True),
    Column('name', String(16)),
    Column('car_number', String(16)),
    Column('driver_1', String(32)),
    Column('driver_2', String(32)),
)


avtomat = Table(
    'avtomat', database_metadata,

    Column('avtomat_number', Integer, primary_key=True),
    Column('house', String(16)),
    Column('latitude', Float),
    Column('longitude', Float),
    Column('search_radius', Integer),
    Column('price', Integer),
    Column('price_for_app', Integer),
    Column('payment_app_url', String(64)),
    Column('payment_gateway_name', String(64)),
    Column('payment_gateway_url', String(64)),
    Column('max_sum', Integer),
    Column('size', Integer),
    Column('competitors', Boolean),
    Column('state', TINYINT(1)),  # 0 - undefined, 1 - normal, 2 - no volt, 3 - crashed
    Column('route_id', Integer, ForeignKey('route.id', ondelete='SET NULL')),
    Column('street_id', Integer, ForeignKey('street.id', ondelete='SET NULL')),
)

status = Table(
    'status', database_metadata,

    Column('id', Integer, primary_key=True),
    Column('time', DateTime),
    Column('money', Integer),
    Column('water', Integer),
    Column('price', Integer),
    Column('time_to_block', Integer),
    Column('grn', Integer),
    Column('kop', Integer),
    Column('money_app', Integer),
    Column('bill_not_work', Integer),
    Column('coin_not_work', Integer),
    Column('low_water_balance', Boolean),  # Low water balance in avtomat
    Column('error_volt', Boolean),  # Troubles with 220V
    Column('error_bill', Boolean),  # Troubles with bill
    Column('error_counter', Boolean),  # Troubles with water counter
    Column('error_register', Boolean),  # Troubles with cash register
    Column('cashbox', Boolean),  # Open (1) or close (0) cashbox
    Column('gsm', Integer),  # Quality of GSM signal. 0 - goog..7-bad, 99 - None
    Column('event', Integer),
    Column('avtomat_number', Integer, ForeignKey('avtomat.avtomat_number', ondelete='CASCADE')),
)
