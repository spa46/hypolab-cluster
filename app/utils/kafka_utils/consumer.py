# app/utils/kafka_utils/consumer.py

import logging
import json
from confluent_kafka import Consumer, KafkaException, KafkaError

logger = logging.getLogger(__name__)

def get_kafka_consumer(bootstrap_servers, auto_offset_reset, group_id):
    """Creates a Kafka consumer."""
    if not bootstrap_servers:
        raise ValueError("Bootstrap servers must be provided")
    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': auto_offset_reset
    })
    logger.info("Kafka consumer created")
    return consumer

def consume_messages(consumer, topic_callbacks):
    """Consumes and processes messages from the Kafka topic."""
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"End of partition reached {msg.partition()}")
                else:
                    raise KafkaException(msg.error())
            else:
                parsed_message = json.loads(msg.value().decode('utf-8'))
                logger.info(f"Message consumed and parsed: {parsed_message}")
                # Call the appropriate callback based on the topic
                topic = msg.topic()
                if topic in topic_callbacks:
                    topic_callbacks[topic](parsed_message)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()