"""
Notifier Service - Business logic for sending notifications.
Implements the Fan-Out pattern for user notifications when new videos are found.
"""
from src.schemas.events import VideoFoundEvent
from src.repositories.subscription import SubscriptionRepository


class NotifierService:
    """
    Service for handling video notification events.
    Sends notifications to subscribed users when new videos are discovered.
    """
    
    def __init__(self, user_subcription_repo: SubscriptionRepository):
        self.user_subcription_repo = user_subcription_repo

    async def handle_event(self, event: VideoFoundEvent):
        """
        The main handler triggered by the Kafka Consumer.
        Processes VideoFoundEvent and notifies subscribed users.
        """

        video = event.payload

        print(f"🔔 Processing Notification for Video: {video.platform_id} (@{video.author_username})")

        subscribers = await self.user_subcription_repo.get_subscribers_for_account(video.author_username)

        if not subscribers:
            print(f"  🤷 No subscribers found for @{video.author_username}")
            return

        for user in subscribers:
            await self.send_email(user, video)

    async def send_email(self, user, video):
        """
        Send email notification to a user.
        In production, this would integrate with an email service.
        """
        print("  --------------------------------------------------")
        print(f"  📧 TO: {user.email}")
        print(f"  SUBJECT: New TikTok from @{video.author_username}!")
        print(f"  BODY: Check it out here -> {video.video_url}")
        print("  --------------------------------------------------")
