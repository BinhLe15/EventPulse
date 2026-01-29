"""
User repository with user-specific queries.
Handles user CRUD and subscription queries.
"""
from src.utils.get_off_limit import get_off_limit
from src.schemas.user import UserParams
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import UserModel
from src.models.subscription import SubscriptionModel
from src.models.account import MonitoredAccountModel
from src.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """Repository for User model operations."""

    async def get_by_email(self, db: AsyncSession, email: str) -> UserModel | None:
        """Find a user by email address."""
        result = await db.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()

    async def get_all_users(self, db: AsyncSession, params: UserParams) -> Sequence[UserModel]:
        """Get all users."""
        offset, limit = get_off_limit(params.page, params.size)

        stmt = select(UserModel).offset(offset).limit(limit)
        result = await db.execute(stmt)

        return result.scalars().all()

    async def get_active_users(self, db: AsyncSession) -> Sequence[UserModel]:
        """Get all active users."""
        result = await db.execute(select(UserModel).where(UserModel.is_active.is_(True)))
        return result.scalars().all()

    async def get_subscribers_by_account_username(self, db: AsyncSession, username: str) -> Sequence[UserModel]:
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
        result = await db.execute(stmt)
        return result.scalars().all()

user_repo = UserRepository(UserModel)