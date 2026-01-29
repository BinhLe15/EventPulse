# src/worker.py
import asyncio

from src.core.db import AsyncSessionLocal
from src.core.kafka import EventConsumer
from src.repositories.subscription import SubscriptionRepository
from src.services.notifier_service import NotifierService
from src.schemas.events import VideoFoundEvent

async def run_worker():
    # 1. Initialize Infrastructure
    # We use a dedicated group_id so we can scale this worker independently
    consumer = EventConsumer(topic="video.found", group_id="notifications_service")
    await consumer.start_consumer()

    print("🚀 Notifier Worker Started (Clean Arch). Waiting for events...")

    async def event_processor(payload: dict):
        """
        Callback wrapper to ensure every event gets a FRESH DB session.
        This prevents stale data issues.
        """
        async with AsyncSessionLocal() as session:
            # Dependency Injection
            repo = SubscriptionRepository(session)
            service = NotifierService(repo)
            
            # Convert Dict -> Pydantic Schema
            try:
                event = VideoFoundEvent(**payload)
                await service.handle_event(event)
            except Exception as e:
                print(f"❌ Error processing event: {e}")

    try:
        # 2. Start the Loop
        await consumer.consume_events(event_processor)
    except KeyboardInterrupt:
        print("🛑 Stopping Worker...")
    finally:
        await consumer.stop_consumer()

if __name__ == "__main__":
    asyncio.run(run_worker())