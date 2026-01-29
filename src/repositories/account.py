"""
Monitored Account repository.
Handles CRUD operations for monitored TikTok accounts.
"""
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.account import MonitoredAccountModel
from src.repositories.base import BaseRepository


class MonitoredAccountRepository(BaseRepository[MonitoredAccountModel]):
    """Repository for MonitoredAccount model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, MonitoredAccountModel)

    async def get_by_username(self, username: str) -> MonitoredAccountModel | None:
        """Find a monitored account by username."""
        result = await self.db.execute(
            select(MonitoredAccountModel).where(MonitoredAccountModel.username == username)
        )
        return result.scalar_one_or_none()

    async def get_active_accounts(self) -> Sequence[MonitoredAccountModel]:
        """Get all active monitored accounts."""
        result = await self.db.execute(
            select(MonitoredAccountModel).where(MonitoredAccountModel.is_active.is_(True))
        )
        return result.scalars().all()
