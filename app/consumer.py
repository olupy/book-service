import json
import asyncio
from confluent_kafka import Consumer, KafkaException
from database import books_collection
from config import settings
import threading
from typing import Optional

KAFKA_CONFIG: dict[str, str] = {
    "bootstrap.servers": settings.KAFKA_BROKER_URL,
    "group.id": "book_creation_group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(KAFKA_CONFIG)
TOPIC: str = "book_created_topic"

async def consume_books():
    """Kafka consumer that listens for book creation events"""
    consumer.subscribe([TOPIC])
    print(f"Listening to Kafka topic: {TOPIC}")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaException._PARTITION_EOF:
                    continue
                else:
                    print(f"Kafka error: {msg.error()}")
                    continue

            try:
                event_data = json.loads(msg.value().decode("utf-8"))
                await save_book(event_data)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")

    except KeyboardInterrupt:
        print("Consumer stopped manually")
    finally:
        consumer.close()

async def save_book(event_data):
    """Save the received book data"""
    if event_data.get("event") != "BOOK_CREATED":
        print(f"Ignoring event: {event_data.get('event')}")
        return

    book_data: dict[str, Optional[str]] = {
        "producer_id": event_data.get("id"),
        "title": event_data.get("title"),
        "author": event_data.get("author"),
        "publication_date": event_data.get("publication_date"),
        "isbn": event_data.get("isbn"),
        "is_available": event_data.get("is_available"),
        "genre": event_data.get("genre"),
        "language": event_data.get("language"),
        "sub_category": event_data.get("sub_category"),
        "publisher": event_data.get("publisher"),
        "file": event_data.get("file"),
        "cover_image": event_data.get("cover_image")
    }

    # Insert into the db
    await books_collection.insert_one(book_data)
    print(f"Book '{event_data['title']}' stored in Frontend api db.")

def start_kafka_consumer():
    """Runs the Kafka consumer in a separate background thread"""
    def run_async_consumer():
        asyncio.run(consume_books())

    thread = threading.Thread(target=run_async_consumer, daemon=True)
    thread.start()