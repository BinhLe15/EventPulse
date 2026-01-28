# src/domain/events/video_events.py
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field
from src.domain.models import TikTokVideo

class BaseEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_name: str

class VideoFoundEvent(BaseEvent):
    """
    The 'Contract': This event is fired when the Tracker finds a new video.
    Consumers (Notifier, Reposter) will subscribe to this.
    """
    event_name: Literal["video.found"] = "video.found"
    payload: TikTokVideo