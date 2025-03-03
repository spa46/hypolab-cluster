from app.utils.kafka_utils import get_kafka_producer, get_kafka_consumer, send_message, consume_messages
import logging
import os

logger = logging.getLogger(__name__)

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

def register_cluster(data):
    # Create the lock file after registration
    with open(LOCK_FILE, 'w') as f:
        f.write('')
    logger.info('Device registered and lock file created.')
    # producer = get_kafka_producer(bootstrap_servers)
    # send_message(producer, 'register_hypo_cluster', data['id'])
    return {'message': 'Hypo cluster registered successfully'}

def start_kafka_consumer():
    consumer = get_kafka_consumer(bootstrap_servers, 'earliest', 'register')
    topic_callbacks = {
        'register': register_cluster,
        # Add other topics and their corresponding callbacks here
    }
    consume_messages(consumer, topic_callbacks)

# Call start_kafka_consumer to start consuming messages
start_kafka_consumer()