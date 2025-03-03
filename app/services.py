from app.utils.kafka_utils import get_kafka_producer, get_kafka_consumer, send_message, consume_messages
import logging
import os

logger = logging.getLogger(__name__)

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")

def register_hypo_cluster(data):
    producer = get_kafka_producer(bootstrap_servers)
    send_message(producer, 'register_hypo_cluster', data['id'])
    return {'message': 'Hypo cluster registered successfully'}

def get_hypo_cluster_status():
    consumer = get_kafka_consumer(bootstrap_servers, 'earliest', 'status_hypo_cluster')
    messages = consume_messages(consumer)
    return {'status': messages}

def control_hypo_cluster(data):
    producer = get_kafka_producer(bootstrap_servers)
    send_message(producer, 'control_hypo_cluster', data['id'])
    return {'message': 'Hypo cluster control command sent'}

def monitor_hypo_cluster():
    consumer = get_kafka_consumer(bootstrap_servers, 'earliest', 'monitor_hypo_cluster')
    messages = consume_messages(consumer)
    return {'monitor': messages}