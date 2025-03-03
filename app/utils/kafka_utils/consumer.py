import os
import logging
from confluent_kafka import Consumer, KafkaException, KafkaError

logger = logging.getLogger(__name__)

def get_kafka_consumer(bootstrap_servers, auto_offset_reset, topic):
    """Creates a Kafka consumer."""
    group_id = os.getenv("KAFKA_GROUP_ID")
    if not group_id:
        raise ValueError("Group ID must be provided")

    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': auto_offset_reset
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe([topic])
    logger.info(f"Kafka consumer subscribed to topic {topic}")
    return consumer

def consume_messages(consumer):
    """Consumes messages from the Kafka topic."""
    messages = []
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                logger.info(f"End of partition reached {msg.partition()}")
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            messages.append(msg.value().decode('utf-8'))
            logger.info(f"Message consumed: {msg.value().decode('utf-8')}")
    return messages