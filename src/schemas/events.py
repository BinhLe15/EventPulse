"""
Event schemas for domain events.
Used for event-driven communication between services.
"""
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Literal
from pydantic import BaseModel, Field
from src.schemas.video import TikTokVideo


class BaseEvent(BaseModel):
    """
    Base class for all domain events.
    """
    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_name: str


class VideoFoundEvent(BaseEvent):
    """
    Event fired when the Tracker finds a new video.
    Consumers (Notifier, Reposter) subscribe to this event.
    """
    event_name: Literal["video.found"] = "video.found"
    payload: TikTokVideo
