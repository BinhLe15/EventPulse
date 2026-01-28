from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.database.session import get_db

# Repositories
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.monitored_account import MonitoredAccountRepository
from src.infrastructure.repositories.subscription import SubscriptionRepository
from src.infrastructure.repositories.processed_video import ProcessedVideoRepository

# Services
from src.domain_services.notifier.service import NotifierService
from src.domain_services.tracker.service import TrackerService
from src.infrastructure.kafka.producer import EventProducer

# --- Repositories ---

async def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

async def get_monitored_account_repo(db: AsyncSession = Depends(get_db)) -> MonitoredAccountRepository:
    return MonitoredAccountRepository(db)

async def get_subscription_repo(db: AsyncSession = Depends(get_db)) -> SubscriptionRepository:
    return SubscriptionRepository(db)

async def get_processed_video_repo(db: AsyncSession = Depends(get_db)) -> ProcessedVideoRepository:
    return ProcessedVideoRepository(db)

# --- Services ---

async def get_notifier_service(
    user_repo: UserRepository = Depends(get_user_repo)
) -> NotifierService:
    return NotifierService(user_repo)

async def get_event_producer() -> EventProducer:
    return EventProducer()

async def get_tracker_service(
    account_repo: MonitoredAccountRepository = Depends(get_monitored_account_repo),
    video_repo: ProcessedVideoRepository = Depends(get_processed_video_repo),
    producer: EventProducer = Depends(get_event_producer)
) -> TrackerService:
    return TrackerService(account_repo, video_repo, producer)
