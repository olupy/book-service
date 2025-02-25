import json
import logging
from typing import Optional, Any

from django.core.management.base import BaseCommand
from confluent_kafka import Consumer, KafkaError
from library.models import Borrow, Book
from user.models import User
from django.conf import settings

logger = logging.getLogger(__name__)

TOPIC = "borrow_book_topic"

class Command(BaseCommand):
    help = "Kafka Consumer for Borrow Events"

    def handle(self, *args, **options):
        """Start the Kafka consumer and process messages."""
        logger.info("Starting Kafka Consumer for Borrow Events")
        self.stdout.write(self.style.SUCCESS("Kafka Consumer Started"))
        settings.KAFKA_CONFIG["group.id"] = "borrow_book_group"
        consumer = Consumer(
            settings.KAFKA_CONFIG)
        consumer.subscribe([TOPIC])

        self.stdout.write(self.style.SUCCESS(f"Listening to topic: {TOPIC}"))

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    logger.error(f"Kafka error: {msg.error()}")
                    continue

                try:
                    borrow_data = json.loads(msg.value().decode("utf-8"))
                    self.process_borrow(borrow_data)
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()

    def process_borrow(self, data: dict[str, Any]):
        """Process and store the borrow record."""
        try:
            borrow_id: Optional[str]= data.get("borrow_id")
            if not borrow_id:
                logger.error("Missing borrow ID in message")
                return

            if Borrow.objects.filter(id=borrow_id).exists():
                logger.info(f"Borrow record already exists: {borrow_id}")
                return

            book: Optional[Book] = Book.objects.filter(id=data["book_id"], is_available=True).first()
            user: Optional[User] = User.objects.filter(email=data["user_email"]).first()

            if not book:
                logger.error(f"Book not found for ID: {borrow_id}")
                return
            if not user:
                logger.error(f"User not found for ID: {borrow_id}")
                return

            borrow: Borrow = Borrow(
                id=borrow_id,
                book=book,
                user=user,
                borrow_date=data["borrow_date"],
                return_date=data["return_date"],
                is_active=True,
                is_returned=False,
                is_overdue=False
            )
            borrow.save()

            # Mark book as unavailable to make sure things are up to date
            book.is_available = False
            book.save(update_fields = ["is_available"])

            logger.info(f"Successfully saved borrow record: {borrow_id}")

        except Exception as e:
            logger.error(f"Error saving borrow data: {e}")
