import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
CLIENT_ID = "client_1"
STATUS_TOPIC = f"clients/{CLIENT_ID}/status"

def on_connect(client, userdata, flags, reason_code):
    print(f"[{CLIENT_ID}] Connected with Reason Code: {reason_code}")
    client.publish(STATUS_TOPIC, "online", qos=1, retain=True)

def on_disconnect(client, userdata, reason_code):
    print(f"[{CLIENT_ID}] Disconnected with Reason Code: {reason_code}")

client = mqtt.Client(client_id=CLIENT_ID)  # 여기 수정

# LWT 설정 (비정상 종료 시 자동으로 "offline" 메시지 전송)
client.will_set(STATUS_TOPIC, "offline", qos=1, retain=True)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(BROKER, PORT, 60)
client.loop_forever()
