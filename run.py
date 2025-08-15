import sys
import uuid

from mqtt.mqttconnect import mqtt_main

if __name__ == "__main__":
    try:
        id = uuid.uuid4()
        mqtt_main(str(id))
    except KeyboardInterrupt:
        print("MQTT listener terminated")
        sys.exit(0)