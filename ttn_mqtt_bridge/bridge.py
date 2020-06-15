from paho.mqtt import client as mqtt
import time

CONNECTION_WAIT_SLEEP = 5
MQTT_BROKER_ADDRESS = "localhost"
MQTT_TOPIC = "stations/sensor_values"

TTN_BROKER_ADDRESS=""
TTN_TOPIC = "+/devices/+/up"
TTN_USERNAME_APP_ID = ""
TTN_PW_ACCESS_KEY = ""

mqtt_client = mqtt.Client("Bridge")

def mqtt_on_connect(client, userdata, flags, rc):
    global connected  # Use global variable
    connected = False
    if rc == 0:
        print("Connected to Broker")
        connected = True  # Signal connection
    else:
        print("Connection to MQTT Broker failed")

def ttn_on_connect(mqtt_client, userdata, flags, rc):
    global connected  # Use global variable
    connected = False
    if rc == 0:
        print("Connected to TTN MQTT Broker")
        connected = True  # Signal connection
        print("Subscribing to "+TTN_TOPIC+" topic")
        mqtt_client.subscribe(TTN_TOPIC, 1)
    else:
        print("Connection to Broker failed")

def mqtt_on_message(client, userdata, message):
    print("MQTT Message received: " + message.topic + " - " + message.payload)

def ttn_on_message(client, userdata, message):
    print("MQTT Message received from TTN: " + message.topic + " - " + message.payload)
    #mqtt_client.publish(MQTT_TOPIC, m, 1)

def main():
    print("--TTN -> MQTT bridge initialization--")

    print("Initializing MQTT protocol for TTN")
    ttn_mqtt_client=mqtt.Client("Bridge")
    ttn_mqtt_client.on_connect = ttn_on_connect
    ttn_mqtt_client.on_message = ttn_on_message

    print("Connecting to TTN MQTT Broker at " + TTN_BROKER_ADDRESS)
    ttn_mqtt_client.connect(TTN_BROKER_ADDRESS)
    ttn_mqtt_client.loop_start()

    print("Waiting for TTN connection to complete")
    time.sleep(CONNECTION_WAIT_SLEEP)

    print("Initializing MQTT protocol")
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_message = mqtt_on_message

    print("Connecting to MQTT Broker at " + MQTT_BROKER_ADDRESS)
    mqtt_client.connect(MQTT_BROKER_ADDRESS)
    mqtt_client.loop_start()

    print("Waiting for connection to complete")
    time.sleep(CONNECTION_WAIT_SLEEP)

    print("Listening for TTN messages...")
    ttn_mqtt_client.loop_forever()

if __name__ == "__main__":
    main()