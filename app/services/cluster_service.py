
def process_message(client, userdata, msg):
    print(f"Received message on topic {message.topic}: {message.payload.decode()}")