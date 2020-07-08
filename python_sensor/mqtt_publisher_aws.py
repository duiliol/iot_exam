import sys
import time

from paho.mqtt import client as mqtt
from aws.aws_config import *

from python_sensor.virtual_station import Station

SLEEP_TIMER = 10
INTERSENSOR_READ_SLEEP = 1
CONNECTION_WAIT_SLEEP = 5

def on_connect(client, userdata, flags, rc):
    global connected  # Use global variable
    connected = False
    if rc == 0:
        print("Connected to Broker")
        connected = True  # Signal connection
    else:
        print("Connection to Broker failed")

def on_message(client, userdata, message):
    print("Message received: " + message.topic + " - " + message.payload)


def main(number_of_stations):
    number_of_stations = int(number_of_stations)
    if number_of_stations <= 0:
        return
    else:
        print("Starting MQTT Publisher with " + str(number_of_stations) + " virtual stations")
        # Initializing the virtual stations
        stations = []
        for i in range(0, number_of_stations):
            station_identifier = "PY" + str(i)
            new_station = Station(station_identifier)
            print("Initialized station " + new_station.get_station_id())
            stations.append(new_station)

        print("Initializing Mosquitto Client")
        mq_client = mqtt.Client("Station Publisher")
        mq_client.on_connect = on_connect
        mq_client.on_message = on_message

        print("Connecting to Broker")
        mq_client.tls_set(CA_CERTIFICATE, CLIENT_CERTIFICATE, keyfile=PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED,
                            tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        print("Trying connection")
        mq_client.connect(aws_iot_endpoint, BROKERPORT)
        mq_client.loop_start()

        print("Waiting for connection to complete")
        time.sleep(CONNECTION_WAIT_SLEEP)

        # cyclic data generation and publishing
        while True:
            for station in stations:
                station.update_sensors_values()
                sensor_values = station.get_sensors_values()
                print(sensor_values)
                mq_client.publish("stations/sensor_values",sensor_values, 1)
                time.sleep(INTERSENSOR_READ_SLEEP)
            time.sleep(SLEEP_TIMER)


if __name__ == "__main__":
    # Read the number of virtual stations from arguments
    number_of_stations = sys.argv[1]
    # Start main
    main(number_of_stations)
