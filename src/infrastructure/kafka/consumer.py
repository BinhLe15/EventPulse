import json
import os
import asyncio
from aiokafka import AIOKafkaConsumer
from src.domain.events.video_events import BaseEvent

class EventConsumer:
    def __init__(self, topic: str, group_id: str):
        self.bootstrap_servers = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        self.running = False

    async def start_consumer(self):
        """Connect to Kafka."""
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            # Start from the beginning if we miss data
            auto_offset_reset="earliest" 
        )
        await self.consumer.start()
        self.running = True
        print(f"👂 Consumer connected! Listening to '{self.topic}' (Group: {self.group_id})")

    async def stop_consumer(self):
        self.running = False
        if self.consumer:
            await self.consumer.stop()

    async def consume_events(self, callback_func):
        """
        Infinite loop that yields messages to the callback function.
        """
        if not self.consumer:
            raise RuntimeError("Consumer not started!")

        try:
            # The async loop
            async for msg in self.consumer:
                if not self.running:
                    break
                
                if msg.value is None:
                    continue

                try:
                    # 1. Decode JSON
                    payload = json.loads(msg.value.decode('utf-8'))
                    print(f"📨 Received Event ID: {payload.get('event_id')}")
                    
                    # 2. Pass to Business Logic
                    await callback_func(payload)
                    
                except Exception as e:
                    print(f"❌ Error processing message: {e}")
                    # In PROD: Log this to Sentry or a Dead Letter Queue
        finally:
            await self.stop_consumer()