# app/utils/kafka_utils/__init__.py

from .producer import get_kafka_producer, send_message
from .consumer import get_kafka_consumer, consume_messages