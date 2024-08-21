from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from cash_machine.database import get_async_session

from .base import BaseRepository
from .items import ItemsRepository


class Repository(BaseRepository):
    """
    The general repository.
    """

    items: ItemsRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.items = ItemsRepository(session=session)


async def get_repository(
    session: AsyncSession = Depends(get_async_session),
) -> Repository:
    return Repository(session=session)
