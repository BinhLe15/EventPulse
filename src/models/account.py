"""
Monitored Account SQLAlchemy model.
Represents TikTok accounts being tracked for new content.
"""
import uuid
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.video import ProcessedVideoModel
    from src.models.subscription import SubscriptionModel


class MonitoredAccountModel(Base):
    """
    TikTok accounts we want to watch for new videos.
    """
    __tablename__ = "monitored_accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    platform: Mapped[str] = mapped_column(String, default="tiktok", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_scraped_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    videos: Mapped[List["ProcessedVideoModel"]] = relationship(back_populates="account")
    subscribers: Mapped[List["SubscriptionModel"]] = relationship(back_populates="account")

    def __repr__(self):
        return f"<MonitoredAccount(username='{self.username}', active={self.is_active})>"
