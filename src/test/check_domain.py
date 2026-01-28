from src.domain.models import TikTokVideo
from src.domain.events import VideoFoundEvent
from datetime import datetime

# Test Data
data = {
    "platform_id": "12345", 
    "author_username": "test_user", 
    "video_url": "https://tiktok.com/123", 
    "created_at": datetime.now()
}

try:
    # 1. Validate Model
    video = TikTokVideo(**data)
    # 2. Wrap in Event
    event = VideoFoundEvent(payload=video)
    print("✅ Domain Layer is valid!")
    print(event.model_dump_json(indent=2))
except Exception as e:
    print(f"❌ Error: {e}")