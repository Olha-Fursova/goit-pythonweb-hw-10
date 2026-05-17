from datetime import date

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    email: Mapped[str] = mapped_column(String(120), unique=True)

    phone: Mapped[str] = mapped_column(String(20))

    birthday: Mapped[date] = mapped_column(Date)

    additional_data: Mapped[str] = mapped_column(String(250), nullable=True)