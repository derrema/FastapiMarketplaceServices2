from typing import List

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.connection import Base

class Cart(Base):
    __tablename__ = 'cart'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    owner: Mapped[int] = mapped_column(unique=True)

    cart_item: Mapped[List['CartItem']] = relationship(back_populates='item_cart',
                                                       cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Cart(id={self.id!r}, owner={self.owner!r})"

class CartItem(Base):
    __tablename__ = 'cart_item'

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.id'))
    product: Mapped[str] = mapped_column(String)
    quantity: Mapped[int] = mapped_column(Integer, default=1)

    item_cart: Mapped[Cart] = relationship(back_populates='cart_item')

    def __repr__(self) -> str:
        return f'CartItem(id={self.id}, product={self.product}, quantity={self.quantity})'