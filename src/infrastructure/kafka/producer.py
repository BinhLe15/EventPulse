import json
import os
from aiokafka import AIOKafkaProducer
from src.domain.events.video_events import BaseEvent

class EventProducer:
    def __init__(self):
        self.bootstrap_servers = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
        self.producer = None

    async def start_producer(self):
        """Initialize the connection to Kafka."""
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )
        await self.producer.start()
        print(f"✅ Kafka Producer connected to {self.bootstrap_servers}")

    async def stop_producer(self):
        """Gracefully shut down."""
        if self.producer:
            await self.producer.stop()

    async def send_event(self, event: BaseEvent):
        """
        Publishes a Pydantic event to the topic defined in the event itself.
        """
        if not self.producer:
            raise RuntimeError("Producer is not started. Call start_producer() first.")

        topic_name = event.event_name
        
        # 1. Serialize Pydantic to JSON string
        payload_json = event.model_dump_json()
        
        # 2. Encode to bytes (Kafka speaks bytes)
        payload_bytes = payload_json.encode("utf-8")

        try:
            # 3. Send and wait for acknowledgement
            await self.producer.send_and_wait(topic_name, payload_bytes)
            print(f"🚀 Sent event {event.event_id} to topic '{topic_name}'")
        except Exception as e:
            print(f"❌ Failed to send event: {e}")