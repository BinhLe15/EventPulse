"""
Processed Video SQLAlchemy model.
Tracks videos that have already been processed to prevent duplicate notifications.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.account import MonitoredAccountModel


class ProcessedVideoModel(Base):
    """
    Stores IDs of videos we have already sent alerts for.
    Prevents duplicate emails.
    """
    __tablename__ = "processed_videos"

    video_id: Mapped[str] = mapped_column(String, primary_key=True)  # The TikTok Video ID
    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monitored_accounts.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Back reference
    account: Mapped["MonitoredAccountModel"] = relationship(back_populates="videos")

    def __repr__(self):
        return f"<ProcessedVideo(id='{self.video_id}', account_id='{self.account_id}')>"
