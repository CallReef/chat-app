import redis
import json
from typing import Dict, Any
from config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


class RedisManager:
    def __init__(self):
        self.redis = redis_client
    
    def publish_message(self, channel: str, message: Dict[str, Any]):
        """Publish a message to a Redis channel"""
        self.redis.publish(channel, json.dumps(message))
    
    def subscribe_to_channel(self, channel: str):
        """Subscribe to a Redis channel"""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        return pubsub
    
    def get_online_users(self) -> set:
        """Get set of online user IDs"""
        return self.redis.smembers("online_users")
    
    def add_online_user(self, user_id: int):
        """Add user to online users set"""
        self.redis.sadd("online_users", user_id)
    
    def remove_online_user(self, user_id: int):
        """Remove user from online users set"""
        self.redis.srem("online_users", user_id)
    
    def is_user_online(self, user_id: int) -> bool:
        """Check if user is online"""
        return self.redis.sismember("online_users", user_id)
    
    def get_chat_channel(self, user1_id: int, user2_id: int) -> str:
        """Get channel name for 1:1 chat between two users"""
        # Sort IDs to ensure consistent channel naming
        sorted_ids = sorted([user1_id, user2_id])
        return f"chat:{sorted_ids[0]}:{sorted_ids[1]}"
    
    def get_typing_channel(self, user1_id: int, user2_id: int) -> str:
        """Get channel name for typing indicators"""
        sorted_ids = sorted([user1_id, user2_id])
        return f"typing:{sorted_ids[0]}:{sorted_ids[1]}"


redis_manager = RedisManager()
