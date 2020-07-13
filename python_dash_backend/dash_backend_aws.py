import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from paho.mqtt import client as mqtt
from aws.aws_config import *

CONNECTION_WAIT_SLEEP = 5

def on_connect(mqtt_client, userdata, flags, rc):
    global connected  # Use global variable
    connected = False
    if rc == 0:
        print("Connected to Broker")
        connected = True  # Signal connection
        print("Subscribing to sensor_values topic")
        mqtt_client.subscribe("stations/sensor_values", 1)
    else:
        print("Connection to Broker failed")


def on_message(mqtt_client, userdata, message):
    print("Message received: " + message.topic + " - " + message.payload.decode())
    f = open("received_values.txt","a")
    f.write(message.payload.decode() + "\n")
    f.close()

def main():
    #f = open("received_values.txt","w")
    #f.close()
    print("Initializing Mosquitto Client")
    mqtt_client = mqtt.Client("Backend Subscriber")
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    print("Connecting to Broker")
    mqtt_client.tls_set(CA_CERTIFICATE, CLIENT_CERTIFICATE, keyfile=PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED,
                        tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    print("Trying connection")
    mqtt_client.connect(aws_iot_endpoint, BROKERPORT)

    print("Listening...")
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
