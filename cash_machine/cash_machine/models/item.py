from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TEXT, INTEGER
from .base import Base


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = mapped_column(INTEGER(), primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(TEXT())
    price: Mapped[int] = mapped_column(INTEGER(), CheckConstraint('price > 0', name='check_price_positive'))
