from datetime import datetime
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from db.databases import Model


class User(Model):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    last_name: Mapped[str] = mapped_column(String(64))
    first_name: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(128))
    permission: Mapped[str] = mapped_column(String(64))
    city: Mapped[str] = mapped_column(String(64))
    last_visit: Mapped[datetime]

    def __repr__(self):
        return f'User("{self.username}")'
