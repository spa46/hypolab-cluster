import os
from flask_mqtt import Mqtt

mqtt = Mqtt()

def initialize_mqtt(app):
    app.config['MQTT_BROKER_URL'] = os.getenv('MQTT_BROKER_URL', 'localhost')
    app.config['MQTT_BROKER_PORT'] = int(os.getenv('MQTT_BROKER_PORT', 1883))
    app.config['MQTT_USERNAME'] = os.getenv('MQTT_USERNAME', '')  # Set this if you have a username
    app.config['MQTT_PASSWORD'] = os.getenv('MQTT_PASSWORD', '')  # Set this if you have a password
    app.config['MQTT_KEEPALIVE'] = 60
    app.config['MQTT_TLS_ENABLED'] = False
    mqtt.init_app(app)