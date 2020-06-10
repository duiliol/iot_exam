from MQTTSNclient import Callback, Client
from paho.mqtt import client as mqtt
import MQTTSN
import queue
import time

MQTTSN_BROKER_ADDRESS = "localhost"
MQTTSN_BROKER_PORT = 1885
MQTTSN_TOPIC = "sensor_values"

CONNECTION_WAIT_SLEEP = 5
MQTT_BROKER_ADDRESS = "localhost"
MQTT_TOPIC = "stations/sensor_values"

message_queue=queue.Queue()

class BridgeCallback(Callback):
    def messageArrived(self, client, TopicId, payload, qos, retained, msgid):
        message_queue.put(payload)
        return True

def mqtt_on_connect(client, userdata, flags, rc):
    global connected  # Use global variable
    connected = False
    if rc == 0:
        print("Connected to Broker")
        connected = True  # Signal connection
    else:
        print("Connection to MQTT Broker failed")

def mqtt_on_message(client, userdata, message):
    print("MQTT Message received: " + message.topic + " - " + message.payload)
    
def main():
    print("--MQTT-SN -> MQTT bridge initialization--")
    print("Initializing MQTT-SN protocol")
    client = Client("Bridge")
    client.registerCallback(BridgeCallback())
    print("Connecting to MQTT-SN broker at " + MQTTSN_BROKER_ADDRESS + ":" + str(MQTTSN_BROKER_PORT))
    client.connected_flag=False
    client.connect(MQTTSN_BROKER_ADDRESS, MQTTSN_BROKER_PORT)
    client.loop_start()
    while not client.connected_flag:
        time.sleep(5)
        print("Waiting for connection to MQTT-SN broker...")

    print("Initializing MQTT protocol")
    mqtt_client = mqtt.Client("Bridge")
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message

    print("Connecting to MQTT Broker at "+ MQTT_BROKER_ADDRESS)
    mqtt_client.connect(MQTT_BROKER_ADDRESS)
    mqtt_client.loop_start()

    print("Waiting for connection to complete")
    time.sleep(CONNECTION_WAIT_SLEEP)

    client.loop_start()
    
    rc, topic_id = client.subscribe(MQTTSN_TOPIC, 0)
    if rc == 0:
        print("Subscribed to "+MQTTSN_TOPIC+ " MQTT-SN topic.")
    else:
        return -1

    while True:
        while not message_queue.empty():
            m = message_queue.get()
            print(m)
            mqtt_client.publish(MQTT_TOPIC, m, 1)

if __name__ == "__main__":
    main()