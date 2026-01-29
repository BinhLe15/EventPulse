"""
Processed Video repository.
Tracks which videos have already been processed to prevent duplicates.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.video import ProcessedVideoModel
from src.repositories.base import BaseRepository


class ProcessedVideoRepository(BaseRepository[ProcessedVideoModel]):
    """Repository for ProcessedVideo model operations."""
    
    def __init__(self, db: AsyncSession):
        super().__init__(db, ProcessedVideoModel)

    async def is_video_processed(self, video_id: str) -> bool:
        """Check if a video has already been processed."""
        result = await self.db.execute(
            select(ProcessedVideoModel).where(ProcessedVideoModel.video_id == video_id)
        )
        return result.scalar_one_or_none() is not None
