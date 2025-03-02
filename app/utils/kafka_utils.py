import logging
from confluent_kafka import Producer, Consumer, KafkaException

logger = logging.getLogger(__name__)

def get_kafka_producer():
    producer = Producer({'bootstrap.servers': 'localhost:9092'})
    logger.info("Kafka producer created")
    return producer

def get_kafka_consumer(group_id, topics):
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe(topics)
    logger.info(f"Kafka consumer created for group {group_id} and topics {topics}")
    return consumer

def send_message(producer, topic, message):
    producer.produce(topic, message)
    producer.flush()
    logger.info(f"Message sent to topic {topic}: {message}")

def consume_messages(consumer):
    messages = []
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
            messages.append(msg.value().decode('utf-8'))
            logger.info(f"Message consumed: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        logger.info("Kafka consumer closed")
    return messages