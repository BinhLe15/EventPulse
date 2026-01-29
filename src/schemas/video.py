"""
TikTok Video Pydantic schema.
Core domain model representing a detected video.
"""
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field


class TikTokVideo(BaseModel):
    """
    Core Domain Model: Represents a detected video from TikTok.
    """
    platform_id: str = Field(..., min_length=1, description="Unique ID from TikTok (e.g., '728391...')")
    author_username: str
    caption: str = ""
    video_url: HttpUrl
    cover_image_url: HttpUrl | None = None
    created_at: datetime

    class Config:
        from_attributes = True
