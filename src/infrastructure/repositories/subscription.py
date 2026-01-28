from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.tables import SubscriptionModel
from src.infrastructure.repositories.base import BaseRepository

class SubscriptionRepository(BaseRepository[SubscriptionModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, SubscriptionModel)
