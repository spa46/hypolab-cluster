import logging
from confluent_kafka import Producer

logger = logging.getLogger(__name__)

def get_kafka_producer(bootstrap_servers):
    """Creates a Kafka producer."""
    if not bootstrap_servers:
        raise ValueError("Bootstrap servers must be provided")
    producer = Producer({'bootstrap.servers': bootstrap_servers})
    logger.info("Kafka producer created")
    return producer

def send_message(producer, topic, message):
    """Sends a message to the Kafka topic."""
    producer.produce(topic, message.encode('utf-8'))
    producer.flush()
    logger.info(f"Message sent to {topic}: {message}")