import asyncio
from unittest.mock import MagicMock
from src.infrastructure.repositories.user import UserRepository
from src.infrastructure.repositories.monitored_account import MonitoredAccountRepository
from src.services.notifier.service import NotifierService
from src.services.tracker.service import TrackerService
from src.infrastructure.repositories.processed_video import ProcessedVideoRepository

async def verify_instantiation():
    mock_session = MagicMock()
    
    # Repos
    user_repo = UserRepository(mock_session)
    account_repo = MonitoredAccountRepository(mock_session)
    video_repo = ProcessedVideoRepository(mock_session)
    
    # Services
    notifier = NotifierService(user_repo)
    tracker = TrackerService(account_repo, video_repo, MagicMock())
    
    print("Classes instantiated successfully.")

if __name__ == "__main__":
    asyncio.run(verify_instantiation())
