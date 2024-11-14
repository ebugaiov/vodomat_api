from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Model
from api.v2.models import City


class Street(Model):
    __tablename__ = 'street'

    id: Mapped[int] = mapped_column(primary_key=True)
    street: Mapped[str] = mapped_column(String(64), index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'), index=True)

    city: Mapped['City'] = relationship(back_populates='streets')
