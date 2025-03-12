import os
import logging
from dotenv import load_dotenv
from flask_mqtt import Mqtt

mqtt = Mqtt()
logger = logging.getLogger(__name__)

client_id = '12345678'
CONNECTIONS = f'clusters/{client_id}/connections'
STATUS = f'clusters/{client_id}/status'

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    logger.info(f"[{client_id}] Connected with Reason Code: {rc}")
    client.publish(CONNECTIONS, "online", qos=1, retain=True)

    client.subscribe(STATUS, qos=1)

@mqtt.on_disconnect()
def handle_disconnect(client, userdata, rc):
    logger.info(f"[{client_id}] Disconnected with Reason Code: {rc}")

def parse_topic(topic):
    return topic.split('/')[-1]

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    logger.info(f"Received message: {message.payload.decode()} on topic {message.topic}")
    topic = parse_topic(message.topic)

def publish_message(topic, payload):
    mqtt.publish(topic, payload)
    logger.info(f"Published message: {payload} to topic: {topic}")

def initialize_mqtt(app):
    load_dotenv()

    app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL')
    app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT'))
    app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME', '')  # Set this if you have a username
    app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD', '')  # Set this if you have a password
    app.config['MQTT_KEEPALIVE'] = 60
    app.config['MQTT_TLS_ENABLED'] = False

    logger.info(f"MQTT Connected to {app.config['MQTT_BROKER_URL']}:{app.config['MQTT_BROKER_PORT']}")

    # Set Last Will and Testament (LWT) before connecting
    mqtt.client.will_set(CONNECTIONS, "offline", qos=1, retain=True)

    mqtt.init_app(app)

    return mqtt