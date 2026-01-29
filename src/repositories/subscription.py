from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import UserModel
from src.models.subscription import SubscriptionModel
from src.models.account import MonitoredAccountModel

class SubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_subscribers_for_account(self, tiktok_username: str):
        """
        Finds all Users subscribed to the given TikTok username.
        """
        stmt = (
            select(UserModel)
            .join(SubscriptionModel)
            .join(MonitoredAccountModel)
            .where(MonitoredAccountModel.username == tiktok_username)
            .where(UserModel.is_active)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()