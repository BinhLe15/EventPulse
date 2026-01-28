from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.tables import MonitoredAccountModel
from src.infrastructure.repositories.base import BaseRepository

class MonitoredAccountRepository(BaseRepository[MonitoredAccountModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, MonitoredAccountModel)

    async def get_by_username(self, username: str) -> MonitoredAccountModel | None:
        result = await self.db.execute(select(MonitoredAccountModel).where(MonitoredAccountModel.username == username))
        return result.scalar_one_or_none()

    async def get_active_accounts(self) -> Sequence[MonitoredAccountModel]:
        result = await self.db.execute(
            select(MonitoredAccountModel).where(MonitoredAccountModel.is_active.is_(True))
        )
        return result.scalars().all()
