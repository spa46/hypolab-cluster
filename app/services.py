import os
import sys
import logging
import requests

from dotenv import load_dotenv

from app.utils import utils
from app.mqtt import mqtt
# from app.mock_config import mqtt


logger = logging.getLogger(__name__)


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    topic = os.getenv('topic')
    logger.info(f"Connected to MQTT SUB TOPIC: {topic}")
    mqtt.subscribe(topic)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    logger.info(f"Received message: {message.payload.decode()} on topic {message.topic}")


def init_cluster(lock_file):
    utils.save_to_dotenv('server_url', 'http://localhost:8000')
    utils.save_to_dotenv('topic', 'test')
    load_dotenv()
    url = os.getenv('server_url')
    topic = os.getenv('topic')

    try:
        if not topic:
            response = requests.post(f'{url}/api/clusters/init-cluster/')
            logger.info("Registration request sent")
        else:
            response = requests.post(f'{url}/api/clusters/init-cluster/', json={'id': topic})
            logger.info("Registration already registered")

        if response.status_code == 200:
            logger.info("Registration Successful.")
            utils.save_to_dotenv('topic', response.json()['id'])
            # change_subscription(os.getenv('topic'))

            utils.create_lock_file(lock_file)
            logger.info('Device registered and lock file created.')

            utils.restart_server()
        else:
            logger.error(f"Registration request failed with status code: {response.status_code}")
            sys.exit(1)
    except requests.RequestException as e:
        logger.error(f"Registration failed with exception: {e}")
        sys.exit(1)

    # Create the lock file after registration

    return {'message': 'Hypo cluster registered successfully'}


def publish_message(topic, payload):
    mqtt.publish(topic, payload)
    logger.info(f"Published message: {payload} to topic: {topic}")


def parse_message():
    pass