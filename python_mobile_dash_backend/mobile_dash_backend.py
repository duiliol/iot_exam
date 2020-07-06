import time

from paho.mqtt import client as mqtt

BROKERADDRESS = "localhost"
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
    mqtt_client.connect(BROKERADDRESS)

    print("Listening...")
    mqtt_client.loop_forever()


if __name__ == "__main__":
    main()
