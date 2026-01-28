from src.domain.models.video import TikTokVideo
from src.infrastructure.kafka.producer import EventProducer
from src.infrastructure.repositories.monitored_account import MonitoredAccountRepository
from src.infrastructure.repositories.processed_video import ProcessedVideoRepository
from src.infrastructure.database.tables import MonitoredAccountModel, ProcessedVideoModel

# Placeholder for api
from TikTokApi import TikTokApi

class TrackerService:
    def __init__(self, 
                 account_repo: MonitoredAccountRepository, 
                 video_repo: ProcessedVideoRepository, 
                 producer: EventProducer):
        self.account_repo = account_repo
        self.video_repo = video_repo
        self.producer = producer
        self.api = TikTokApi()

    async def get_active_accounts(self):
        return await self.account_repo.get_active_accounts()

    async def is_video_processed(self, video_id: str) -> bool:
        return await self.video_repo.is_video_processed(video_id)

    async def mark_video_processed(self, video: TikTokVideo, account_id):
        new_entry = ProcessedVideoModel(
            video_id=video.platform_id, 
            account_id=account_id
        )
        self.video_repo.add(new_entry)
        await self.video_repo.commit()

    async def process_account(self, account: MonitoredAccountModel):
        print(f"🔎 Checking @{account.username}...")
        # Mock logic
        pass