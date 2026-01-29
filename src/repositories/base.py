"""
Base repository with generic CRUD operations.
Provides standard database operations to avoid boilerplate.
"""
from typing import Generic, TypeVar, Optional, Type, Sequence, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Abstract Base Repository for SQLAlchemy models.
    Provides standard CRUD operations to avoid boilerplate in specific repositories.
    """
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Fetch a single record by its ID.
        """
        # We use getattr to safely access 'id' as the base class might not explicitly define it,
        # resolving the type checker warning.
        model_id = getattr(self.model, 'id')
        result = await db.execute(select(self.model).where(model_id == id))
        return result.scalar_one_or_none()

    async def list(self, db: AsyncSession) -> Sequence[ModelType]:
        """
        Fetch all records for this model.
        """
        result = await db.execute(select(self.model))
        return result.scalars().all()

    def add(self, db: AsyncSession, obj: ModelType) -> ModelType:
        """
        Add a new object to the session.
        Note: You must call commit() to persist changes.
        """
        db.add(obj)
        return obj

    async def delete(self, db: AsyncSession, id: Any) -> None:
        """
        Delete a record by its ID.
        """
        model_id = getattr(self.model, 'id')
        await db.execute(delete(self.model).where(model_id == id))
    
    async def commit(self, db: AsyncSession):
        """
        Commit the current transaction.
        """
        await db.commit()
