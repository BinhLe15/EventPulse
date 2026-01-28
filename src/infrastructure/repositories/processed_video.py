from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.tables import ProcessedVideoModel
from src.infrastructure.repositories.base import BaseRepository

class ProcessedVideoRepository(BaseRepository[ProcessedVideoModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, ProcessedVideoModel)

    async def is_video_processed(self, video_id: str) -> bool:
        result = await self.db.execute(
            select(ProcessedVideoModel).where(ProcessedVideoModel.video_id == video_id)
        )
        return result.scalar_one_or_none() is not None
