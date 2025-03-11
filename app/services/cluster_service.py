import os
import logging
from mqtt.utils.mqtt import mqtt


logger = logging.getLogger(__name__)


CONNECTIONS = 'clusters/12345678/connections'

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    topic = os.getenv('topic')
    logger.info(f"Connected to MQTT SUB TOPIC: {CONNECTIONS}")
    mqtt.subscribe(topic)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    logger.info(f"Received message: {message.payload.decode()} on topic {message.topic}")


def publish_message(topic, payload):
    mqtt.publish(topic, payload)
    logger.info(f"Published message: {payload} to topic: {topic}")