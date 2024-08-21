from sqlalchemy import select

from cash_machine.models import Item
from .base import BaseRepository


class ItemsRepository(BaseRepository):

    async def get(self, item_id: int) -> Item | None:
        stmt = select(Item).where(Item.id == item_id)
        return await self._session.scalar(stmt)

    async def create(self, title: str, price: int) -> Item:
        item = Item(title=title, price=price)
        self._session.add(item)
        await self._session.commit()
        return item

    async def get_all(self) -> list[Item]:
        stmt = select(Item)
        result = await self._session.scalars(stmt)

        if result is not None:
            items = result.all()
        else:
            items = []

        return items
