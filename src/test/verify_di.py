import asyncio
from unittest.mock import MagicMock
from src.domain_services.api.dependencies import get_tracker_service, get_notifier_service
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.monitored_account import MonitoredAccountRepository
from src.infrastructure.repositories.processed_video import ProcessedVideoRepository
from src.infrastructure.kafka.producer import EventProducer

async def verify_di_logic():
    print("Verifying DI factory functions manually...")
    
    # Mock Dependencies
    mock_db = MagicMock()
    user_repo = UserRepository(mock_db)
    account_repo = MonitoredAccountRepository(mock_db)
    video_repo = ProcessedVideoRepository(mock_db)
    producer = EventProducer()

    # Verify Service Creation
    notifier = await get_notifier_service(user_repo)
    tracker = await get_tracker_service(account_repo, video_repo, producer)
    
    assert notifier.user_repo == user_repo
    assert tracker.account_repo == account_repo
    
    print("✅ DI factory functions work correctly.")

if __name__ == "__main__":
    asyncio.run(verify_di_logic())
