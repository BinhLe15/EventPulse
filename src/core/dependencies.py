"""
Dependency Injection for FastAPI.
Provides repository and service instances to API endpoints.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db

# Repositories
from src.repositories.user import UserRepository
from src.repositories.account import MonitoredAccountRepository
from src.repositories.subscription import SubscriptionRepository
from src.repositories.video import ProcessedVideoRepository

# Services
from src.services.notifier_service import NotifierService
from src.services.tracker_service import TrackerService
from src.core.kafka import EventProducer


# --- Repository Dependencies ---

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Provide UserRepository instance."""
    return UserRepository(db)


async def get_monitored_account_repo(db: AsyncSession = Depends(get_db)) -> MonitoredAccountRepository:
    """Provide MonitoredAccountRepository instance."""
    return MonitoredAccountRepository(db)


async def get_subscription_repo(db: AsyncSession = Depends(get_db)) -> SubscriptionRepository:
    """Provide SubscriptionRepository instance."""
    return SubscriptionRepository(db)


async def get_processed_video_repo(db: AsyncSession = Depends(get_db)) -> ProcessedVideoRepository:
    """Provide ProcessedVideoRepository instance."""
    return ProcessedVideoRepository(db)


# --- Service Dependencies ---

async def get_notifier_service(
    user_repo: UserRepository = Depends(get_user_repo)
) -> NotifierService:
    """Provide NotifierService instance with injected dependencies."""
    return NotifierService(user_repo)


async def get_event_producer() -> EventProducer:
    """Provide EventProducer instance."""
    return EventProducer()


async def get_tracker_service(
    account_repo: MonitoredAccountRepository = Depends(get_monitored_account_repo),
    video_repo: ProcessedVideoRepository = Depends(get_processed_video_repo),
    producer: EventProducer = Depends(get_event_producer)
) -> TrackerService:
    """Provide TrackerService instance with injected dependencies."""
    return TrackerService(account_repo, video_repo, producer)
