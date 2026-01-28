from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.tables import UserModel, SubscriptionModel, MonitoredAccountModel
from src.infrastructure.repositories.base import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, UserModel)

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()

    async def get_active_users(self) -> Sequence[UserModel]:
        result = await self.db.execute(select(UserModel).where(UserModel.is_active.is_(True)))
        return result.scalars().all()

    async def get_subscribers_by_account_username(self, username: str) -> Sequence[UserModel]:
        """
        Find all active users subscribed to the account with the given username.
        """
        stmt = (
            select(UserModel)
            .join(SubscriptionModel)
            .join(MonitoredAccountModel)
            .where(MonitoredAccountModel.username == username)
            .where(UserModel.is_active.is_(True))
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()


