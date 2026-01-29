"""
User and Subscription SQLAlchemy models.
Handles user accounts and their subscriptions to monitored accounts.
"""
import uuid
from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.subscription import SubscriptionModel


class UserModel(Base):
    """
    User accounts in the system.
    Users can subscribe to monitored accounts to receive notifications.
    """
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationship: A user has many subscriptions
    subscriptions: Mapped[List["SubscriptionModel"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
