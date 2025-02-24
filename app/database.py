from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from confluent_kafka import Producer
import json
from typing import Any

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client.get_database("fastapi_book_db")

# Collections
users_collection = db.get_collection("users")
books_collection = db.get_collection("books")
borrow_collection = db.get_collection("borrow")

kafka_producer = Producer({
    "bootstrap.servers": settings.KAFKA_BROKER_URL
})

def send_kafka_event(topic: str, message: dict[str, Any]):
    """Send an event to Kafka like say a user has been created."""
    kafka_producer.produce(topic, key=str(message.get("event")), value=json.dumps(message))
    kafka_producer.flush()
