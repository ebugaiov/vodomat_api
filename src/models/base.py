from sqlalchemy.orm import declarative_base

_Base = declarative_base()


class Base(_Base):
    __abstract__ = True

