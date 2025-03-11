import os
import logging

from dotenv import load_dotenv
from flask_mqtt import Mqtt


mqtt = Mqtt()

logger = logging.getLogger(__name__)


def initialize_mqtt(app):
    load_dotenv()

    app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL')
    app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT'))
    app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME', '')  # Set this if you have a username
    app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD', '')  # Set this if you have a password
    app.config['MQTT_KEEPALIVE'] = 60
    app.config['MQTT_TLS_ENABLED'] = False

    logger.info(f"MQTT Connected to {app.config['MQTT_BROKER_URL']}:{app.config['MQTT_BROKER_PORT']}")

    mqtt.init_app(app)

    return mqtt