"""
Tracker Service - Business logic for monitoring TikTok accounts.
Implements the Fan-Out pattern for video discovery and event publishing.
"""
from src.schemas.video import TikTokVideo
from src.core.kafka import EventProducer
from src.repositories.account import MonitoredAccountRepository
from src.repositories.video import ProcessedVideoRepository
from src.models.account import MonitoredAccountModel
from src.models.video import ProcessedVideoModel

# Placeholder for TikTok API
from TikTokApi import TikTokApi


class TrackerService:
    """
    Service for tracking monitored accounts and discovering new videos.
    Uses repository pattern for data access and event producer for notifications.
    """
    
    def __init__(
        self, 
        account_repo: MonitoredAccountRepository, 
        video_repo: ProcessedVideoRepository, 
        producer: EventProducer
    ):
        self.account_repo = account_repo
        self.video_repo = video_repo
        self.producer = producer
        self.api = TikTokApi()

    async def get_active_accounts(self):
        """Get all active monitored accounts."""
        return await self.account_repo.get_active_accounts()

    async def is_video_processed(self, video_id: str) -> bool:
        """Check if a video has already been processed."""
        return await self.video_repo.is_video_processed(video_id)

    async def mark_video_processed(self, video: TikTokVideo, account_id):
        """
        Mark a video as processed to prevent duplicate notifications.
        """
        new_entry = ProcessedVideoModel(
            video_id=video.platform_id, 
            account_id=account_id
        )
        self.video_repo.add(new_entry)
        await self.video_repo.commit()

    async def process_account(self, account: MonitoredAccountModel):
        """
        Process a single monitored account.
        This is where the actual TikTok scraping logic would go.
        """
        print(f"🔎 Checking @{account.username}...")
        # Mock logic - in production, this would call TikTok API
        pass
