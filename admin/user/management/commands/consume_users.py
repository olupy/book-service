import json
import logging
from confluent_kafka import Consumer, KafkaException
from django.core.management.base import BaseCommand
from user.models import User
from django.conf import settings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Kafka consumer for user registration events"

    def handle(self, *args, **options):
        kafka_config: dict[str, str] = settings.KAFKA_CONFIG
        kafka_config["group.id"] = "user_registration_consumer_group"

        consumer = Consumer(kafka_config)
        topic = "user_registration_topic"
        consumer.subscribe([topic])

        self.stdout.write(self.style.SUCCESS(f"Listening to Kafka topic: {topic}"))

        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        continue
                    else:
                        logger.error(f"Kafka error: {msg.error()}")
                        continue
                try:
                    event_data = json.loads(msg.value().decode('utf-8'))
                    self.save_user(event_data)
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {e}")

        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("Consumer stopped manually"))
        finally:
            consumer.close()

    def save_user(self, event_data):
        if event_data.get("event") != "USER_REGISTERED":
            logger.info(f"Ignoring event: {event_data.get('event')}")
            return

        # we try to extract the message received
        user_id = event_data.get("id")
        email = event_data.get("email")
        firstname = event_data.get("firstname")
        lastname = event_data.get("lastname")
        role = event_data.get("role")
        is_active = event_data.get("is_active", True)
        password = event_data.get("password")

        if not user_id or not email:
            logger.error("Missing required fields in event data")
            return

        # Save user to DB
        user, created = User.objects.update_or_create(
            id=user_id,
            defaults={
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "role": role,
                "is_active": is_active,
                "password": password
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"User {email} created successfully"))
        else:
            self.stdout.write(self.style.SUCCESS(f"User {email} updated successfully"))
