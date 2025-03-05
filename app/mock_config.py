# app/mock_config.py

import os

def set_mock_config():
    os.environ['MQTT_BROKER_URL'] = 'mock_broker_url'
    os.environ['MQTT_BROKER_PORT'] = '1883'
    os.environ['MQTT_USERNAME'] = 'test'
    os.environ['MQTT_PASSWORD'] = 'test'
    os.environ['server_url'] = 'localhost:8000'
    os.environ['topic'] = 'topic'