import os
import logging
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Kafka Configs
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")
GROUP_ID = os.getenv("KAFKA_GROUP_ID")
AUTO_OFFSET_RESET = os.getenv("KAFKA_AUTO_OFFSET_RESET", "earliest")

def get_kafka_producer():
    """Creates a Kafka producer."""
    producer = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})
    logger.info("Kafka producer created")
    return producer

def get_kafka_consumer():
    """Creates a Kafka consumer."""
    consumer_config = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': AUTO_OFFSET_RESET
    }
    consumer = Consumer(consumer_config)
    consumer.subscribe([TOPIC])
    logger.info(f"Kafka consumer subscribed to topic {TOPIC}")
    return consumer

def send_message(producer, message):
    """Sends a message to the Kafka topic."""
    producer.produce(TOPIC, message.encode('utf-8'))
    producer.flush()
    logger.info(f"Message sent to {TOPIC}: {message}")

def consume_messages(consumer):
    """Consumes messages from Kafka."""
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            logger.info(f"Consumed message: {msg.value().decode('utf-8')}")
            return msg.value().decode('utf-8')
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
