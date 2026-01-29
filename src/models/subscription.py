from src.models.base import Base

from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, func
import uuid
from datetime import datetime

if TYPE_CHECKING:
    from src.models.user import UserModel
    from src.models.account import MonitoredAccountModel

class SubscriptionModel(Base):
    """
    Join table: User <-> MonitoredAccount
    Represents a user's subscription to a monitored account.
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