import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationship: A user has many subscriptions
    subscriptions: Mapped[List["SubscriptionModel"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"

class MonitoredAccountModel(Base):
    """
    Table: monitored_accounts
    Stores the TikTok users we want to watch.
    """
    __tablename__ = "monitored_accounts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    platform: Mapped[str] = mapped_column(String, default="tiktok", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_scraped_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationship (Optional but helpful)
    videos: Mapped[List["ProcessedVideoModel"]] = relationship(back_populates="account")
    subscribers: Mapped[List["SubscriptionModel"]] = relationship(back_populates="account")

    def __repr__(self):
        return f"<MonitoredAccount(username='{self.username}', active={self.is_active})>"

class SubscriptionModel(Base):
    """
    Join Table: User <-> MonitoredAccount
    """
    __tablename__ = "subscriptions"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monitored_accounts.id"), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships to access the objects
    user: Mapped["UserModel"] = relationship(back_populates="subscriptions")
    account: Mapped["MonitoredAccountModel"] = relationship(back_populates="subscribers")

    def __repr__(self):
        return f"<Subscription {self.user_id} -> {self.account_id}>"

class ProcessedVideoModel(Base):
    """
    Table: processed_videos
    Stores IDs of videos we have already sent alerts for.
    Prevents duplicate emails.
    """
    __tablename__ = "processed_videos"

    video_id: Mapped[str] = mapped_column(String, primary_key=True)  # The TikTok Video ID (e.g. "72839...")
    account_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("monitored_accounts.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Back reference
    account: Mapped["MonitoredAccountModel"] = relationship(back_populates="videos")

    def __repr__(self):
        return f"<ProcessedVideo(id='{self.video_id}', account_id='{self.account_id}')>"