from confluent_kafka import Producer
from django.conf import settings
from typing import Any
import json

producer = Producer(settings.KAFKA_CONFIG)

def send_kafka_event(topic: str, event_data: dict[str, Any]):
    try:
        producer.produce(topic, key=str(event_data["event"]), value=json.dumps(event_data))
        producer.flush()
    except Exception as e:
        print(f"Error sending Kafka event: {e}")