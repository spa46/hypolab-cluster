import paho.mqtt.client as mqtt
import os

class MqttPublisher:
    def __init__(self, broker_url, broker_port, topic):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker_url, self.broker_port)

    def publish(self, message):
        self.client.publish(self.topic, message)

    def disconnect(self):
        self.client.disconnect()

if __name__ == "__main__":
    broker_url = os.getenv('MQTT_BROKER_URL', 'localhost')
    broker_port = int(os.getenv('MQTT_BROKER_PORT', 1883))
    topic = os.getenv('MQTT_TOPIC', 'test/topic')

    publisher = MqttPublisher(broker_url, broker_port, topic)
    publisher.connect()
    publisher.publish("Hello MQTT")
    publisher.disconnect()