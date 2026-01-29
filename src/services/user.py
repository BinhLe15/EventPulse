from src.schemas.user import UserParams
from src.repositories.user import UserRepository, user_repo
from typing import Sequence
from src.models.user import UserModel
from src.core.db import session_context

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_all_users(self, params: UserParams) -> Sequence[UserModel]:
        """Get all users."""
        async with session_context() as db:
            try:
                return await self.user_repo.get_all_users(db, params)
            except Exception as e:
                raise e

user_service = UserService(user_repo)