"""
Kafka producer and consumer wrapper classes.
Provides event-driven communication infrastructure.
"""
import json
import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from src.core.config import settings


class EventProducer:
    """
    Kafka event producer for publishing domain events.
    """
    def __init__(self):
        self.bootstrap_servers = settings.KAFKA_BROKER_URL
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

    async def send_event(self, event):
        """
        Publishes a Pydantic event to the topic defined in the event itself.
        
        Args:
            event: BaseEvent instance with event_name and payload
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


class EventConsumer:
    """
    Kafka event consumer for subscribing to domain events.
    """
    def __init__(self, topic: str, group_id: str):
        self.bootstrap_servers = settings.KAFKA_BROKER_URL
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
        """Gracefully shut down."""
        self.running = False
        if self.consumer:
            await self.consumer.stop()

    async def consume_events(self, callback_func):
        """
        Infinite loop that yields messages to the callback function.
        
        Args:
            callback_func: Async function to handle each event
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
