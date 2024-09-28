from sqlalchemy import Column
from sqlalchemy import Integer, String, DateTime

from .base import Base


class Issue(Base):
    __tablename__ = 'issue'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, index=True)
    avtomat_number = Column(Integer, index=True)
    address = Column(String(120), index=True)
    issue = Column(String(240))
    comment = Column(String(240))
    email = Column(String(64))
