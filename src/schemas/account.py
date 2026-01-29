"""
Monitored Account Pydantic schemas.
DTOs for account CRUD operations.
"""
from src.core.base_schemas import BasePagination
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AccountParams(BasePagination):
    pass


class AccountBase(BaseModel):
    """Base schema with common fields."""
    username: str = Field(..., min_length=1, description="TikTok username to monitor")
    platform: str = Field(default="tiktok", description="Social media platform")
    is_active: bool = Field(default=True, description="Whether monitoring is active")


class AccountCreate(AccountBase):
    """Schema for creating a new monitored account."""
    pass


class AccountUpdate(BaseModel):
    """Schema for updating an existing monitored account."""
    username: Optional[str] = Field(None, min_length=1)
    platform: Optional[str] = None
    is_active: Optional[bool] = None


class AccountRead(AccountBase):
    """Schema for reading monitored account data."""
    id: uuid.UUID
    last_scraped_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
