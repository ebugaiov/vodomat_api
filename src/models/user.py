from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    last_name = Column(String(64))
    first_name = Column(String(64))
    email = Column(String(120))
    password_hash = Column(String(128), nullable=False)
    permission = Column(String(64), nullable=False)
    city = Column(String(64))
    last_visit = Column(DateTime)
