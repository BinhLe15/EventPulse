from src.domain.events.video_events import VideoFoundEvent
from src.infrastructure.repositories.user import UserRepository

class NotifierService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def handle_event(self, raw_event: dict):
        """
        The main handler triggered by the Kafka Consumer.
        """
        try:
            event = VideoFoundEvent(**raw_event)
            video = event.payload
        except Exception as e:
            print(f"⚠️ Invalid Event Format: {e}")
            return

        print(f"🔔 Processing Notification for Video: {video.platform_id} (@{video.author_username})")

        subscribers = await self.user_repo.get_subscribers_by_account_username(video.author_username)

        if not subscribers:
            print(f"  🤷 No subscribers found for @{video.author_username}")
            return

        for user in subscribers:
            await self.send_email(user, video)

    async def send_email(self, user, video):
        print("  --------------------------------------------------")
        print(f"  📧 TO: {user.email}")
        print(f"  SUBJECT: New TikTok from @{video.author_username}!")
        print(f"  BODY: Check it out here -> {video.video_url}")
        print("  --------------------------------------------------")