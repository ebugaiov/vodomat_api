from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Model
from api.v2.models import Street


class City(Model):
    __tablename__ = 'city'

    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    streets: Mapped[list['Street']] = relationship(back_populates='city')

    def __repr__(self):
        return f'City({self.id} "{self.city}")'
