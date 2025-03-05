import os
import sys
import logging
import requests

from flask import current_app
from dotenv import load_dotenv

from app.utils import utils
from app.mqtt import mqtt


logger = logging.getLogger(__name__)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    topic = os.getenv('topic')
    logger.info(f"Connected with result code {rc}")
    mqtt.subscribe(topic)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    logger.info(f"Received message: {message.payload.decode()} on topic {message.topic}")


def change_subscription(new_topic):
    global current_topic
    mqtt.unsubscribe(current_topic)
    current_topic = new_topic
    mqtt.subscribe(current_topic)
    logger.info(f"Subscribed to new topic: {current_topic}")


def init_cluster():
    utils.save_to_dotenv('server_url', 'localhost')
    load_dotenv()
    url = os.getenv('server_url')

    try:
        response = requests.post(f'{url}/api/clusters/init-cluster/')
        logger.info("Registration request sent")
        if response.status_code == 200:
            logger.info("Registration Successful.")
            utils.save_to_dotenv('topic', response.json()['id'])
            change_subscription(os.getenv('topic'))
        else:
            logger.error(f"Registration request failed with status code: {response.status_code}")
            sys.exit(1)
    except requests.RequestException as e:
        logger.error(f"Registration failed with exception: {e}")
        sys.exit(1)



    # Create the lock file after registration
    with open(LOCK_FILE, 'w') as f:
        f.write('')
    logger.info('Device registered and lock file created.')
    # producer = get_kafka_producer(bootstrap_servers)
    # send_message(producer, 'register_hypo_cluster', data['id'])
    return {'message': 'Hypo cluster registered successfully'}


def publish_message(topic, payload):
    mqtt.publish(topic, payload)
    logger.info(f"Published message: {payload} to topic: {topic}")