import paho.mqtt.client as mqtt
import os

class MqttSubscriber:
    def __init__(self, broker_url, broker_port, topic):
        self.broker_url = broker_url
        self.broker_port = broker_port
        self.topic = topic
        self.client = mqtt.Client()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_url, self.broker_port)

    def start(self):
        self.client.loop_forever()

if __name__ == "__main__":
    broker_url = os.getenv('MQTT_BROKER_URL', 'localhost')
    broker_port = int(os.getenv('MQTT_BROKER_PORT', 1883))
    topic = os.getenv('MQTT_TOPIC', 'test/topic')

    subscriber = MqttSubscriber(broker_url, broker_port, topic)
    subscriber.connect()
    subscriber.start()