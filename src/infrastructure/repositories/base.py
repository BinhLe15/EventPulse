from typing import Generic, TypeVar, Optional, Type, Sequence, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from src.infrastructure.database.tables import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Abstract Base Repository for SQLAlchemy models.
    Provides standard CRUD operations to avoid boilerplate in specific repositories.
    """
    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.db = db
        self.model = model

    async def get(self, id: Any) -> Optional[ModelType]:
        """
        Fetch a single record by its ID.
        """
        # We use getattr to safely access 'id' as the base class might not explicitly define it,
        # resolving the type checker warning.
        model_id = getattr(self.model, 'id')
        result = await self.db.execute(select(self.model).where(model_id == id))
        return result.scalar_one_or_none()

    async def list(self) -> Sequence[ModelType]:
        """
        Fetch all records for this model.
        """
        result = await self.db.execute(select(self.model))
        return result.scalars().all()

    def add(self, obj: ModelType) -> ModelType:
        """
        Add a new object to the session.
        Note: You must call commit() to persist changes.
        """
        self.db.add(obj)
        return obj

    async def delete(self, id: Any) -> None:
        """
        Delete a record by its ID.
        """
        model_id = getattr(self.model, 'id')
        await self.db.execute(delete(self.model).where(model_id == id))
    
    async def commit(self):
        """
        Commit the current transaction.
        """
        await self.db.commit()

base_repository = BaseRepository
