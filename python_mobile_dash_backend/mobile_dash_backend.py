import ssl
import time

from paho.mqtt import client as mqtt
import json
from aws.aws_config import *

CONNECTION_WAIT_SLEEP = 5

def on_mqtt_connect(mqtt_client, userdata, flags, rc):
    global connected  # Use global variable
    connected = False
    #print(rc)
    if rc == 0:
        print("Connected to Broker")
        connected = True  # Signal connection
        print("Subscribing to mobile_sensor_states topic")
        mqtt_client.subscribe("stations/mobile_sensor_states", 1)
    else:
        print("Connection to Broker failed")

def on_mqtt_message(mqtt_client, userdata, message):
    print("Message received: " + message.topic + " - " + message.payload.decode())
    f = open("received_values.txt","a")
    json_state = json.loads(message.payload.decode())
    if("x" not in json_state or "y" not in json_state or "z" not in json_state):
        json_state["x"]="N/A"
        json_state["y"]="N/A"
        json_state["z"]="N/A"
    normalized_message = {
        "id":json_state["id"],
        "time":json_state["time"],
        "x":json_state["x"],
        "y":json_state["y"],
        "z":json_state["z"],
        "state":json_state["state"]
    }
    f.write(json.dumps(normalized_message) + "\n")
    f.close()

def main():
    #f = open("received_values.txt","w")
    #f.close()
    print("Initializing MQTT Client")
    mqtt_client = mqtt.Client()

    mqtt_client.on_connect = on_mqtt_connect
    mqtt_client.on_message = on_mqtt_message

    print("Connecting to Broker")
    print("Setting TLS security")
    #ssl_context = ssl_alpn()
    #mqtt_client.tls_set_context(context=ssl_context)
    mqtt_client.tls_set(CA_CERTIFICATE, CLIENT_CERTIFICATE, keyfile=PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED,
              tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    print("Trying connection")
    mqtt_client.connect(aws_iot_endpoint, BROKERPORT)

    print("Listening...")
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
