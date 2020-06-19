import base64
import json
import time
from datetime import datetime
from ttn_mqtt_bridge.ttn_bridge_conf import *

from paho.mqtt import client as mqtt, publish

mqtt_broker = mqtt.Client("TTN Bridge")

def on_connect(client, userdata, flags, rc):
    global connected  # Use global variable
    connected = False
    if rc == 0:
        print("Connected to TTN Broker")
        connected = True  # Signal connection
        print("Subscribing to "+TTN_TOPIC+" topic")
        client.subscribe(TTN_TOPIC, 1)
    else:
        print("Connection to TTN Broker failed")

def mqtt_broker_on_connect(client, userdata, flags, rc):
    global connected  # Use global variable
    connected = False
    if rc == 0:
        print("Connected to MQTT Broker")
        connected = True  # Signal connection
    else:
        print("Connection to MQTT Broker failed")

def on_message(client, userdata, message):
    print("Message received: " + message.topic + " - " + message.payload.decode())
    recv_json = json.loads(message.payload.decode())
    payload_decode = base64.b64decode(recv_json["payload_raw"])
    payload_json = json.loads(payload_decode)
    new_timestamp = datetime.now()
    payload_json["time"]=new_timestamp.isoformat()
    print("Forwarding to MQTT broker...")
    print(MQTT_TOPIC + ": "+ json.dumps(payload_json))
    publish.single(
        MQTT_TOPIC, payload=json.dumps(payload_json), qos=1, retain=False,
        hostname=BROKERADDRESS, port=1883, client_id='TTN Bridge',
        keepalive=60, will=None, auth=None, tls=None, protocol=mqtt.MQTTv311)
    print("Forward completed.")

def main():
    #f = open("received_values.txt","w")
    #f.close()
    print("Initializing Mosquitto Client")
    mqtt_client = mqtt.Client("TTN Bridge")
    mqtt_client.username_pw_set(TTN_USERNAME_APP_ID,TTN_PW_ACCESS_KEY)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    print("Connecting to Broker")
    mqtt_client.connect(TTN_BROKER_ADDRESS)

    print("Listening...")
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
