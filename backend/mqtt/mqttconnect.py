# mqtt_reader/classes.py

import json
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from orm.operations import upsert_opportunity


# MQTT connection settings
BROKER = "localhost"  # Replace with your broker
PORT = 18883
TOPIC = "learning/topic/opportunity"
USERNAME = "user1"
PASSWORD = "password1"

def on_connect(client, userdata, flags, rc, properties):
    print(properties)
    if rc == 0:
        print("✅ Connected to MQTT broker")
        client.subscribe(TOPIC)
    else:
        print(f"❌ Connection failed with code {rc}")


def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        operation_type, ret_id = upsert_opportunity(payload)

        data = json.loads(payload)
        print(f"Incoming 📩 {msg.topic}: {json.dumps(data, indent=2)}")
        print(f"Data was {operation_type} and id is {ret_id}")
    except json.JSONDecodeError:
        print(f"⚠️ Received non-JSON message on {msg.topic}: {msg.payload.decode()}")



def mqtt_main(identifier: str):
    client = mqtt.Client(
        callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=identifier
    )

    # Set username and password
    client.username_pw_set(USERNAME, PASSWORD)

    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(BROKER, PORT, 60)
    client.loop_forever()

