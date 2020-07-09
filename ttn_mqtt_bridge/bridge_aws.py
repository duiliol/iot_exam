import base64
import json
import time
from datetime import datetime
from ttn_mqtt_bridge.ttn_bridge_conf import *
from aws.aws_config import *

from paho.mqtt import client as mqtt, publish

mqtt_client = mqtt.Client("TTN Bridge")

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
    #ret = publish.single(
        #MQTT_TOPIC, payload=json.dumps(payload_json), qos=1, retain=False,
        #hostname=aws_iot_endpoint, port=BROKERPORT, client_id='TTN Bridge',
        #keepalive=60, will=None, auth=None, tls={'ca_certs':CA_CERTIFICATE, 'certfile':CLIENT_CERTIFICATE, 'keyfile':PRIVATE_KEY, 'tls_version':ssl.PROTOCOL_TLSv1_2, 'ciphers':"None"}, protocol=mqtt.MQTTv311)
    mqtt_client.publish(MQTT_TOPIC, json.dumps(payload_json), 1)
    print("Forward completed.")

def main():
    #f = open("received_values.txt","w")
    #f.close()
    print("Connecting to MQTT Broker")
    mqtt_client.on_connect = mqtt_broker_on_connect

    print("Connecting to Broker")
    mqtt_client.tls_set(CA_CERTIFICATE, CLIENT_CERTIFICATE, keyfile=PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED,
                        tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
    print("Trying MQTT connection")
    mqtt_client.connect(aws_iot_endpoint, BROKERPORT)

    print("Initializing TTN Client")
    ttn_mqtt_client = mqtt.Client("TTN Bridge")
    ttn_mqtt_client.username_pw_set(TTN_USERNAME_APP_ID,TTN_PW_ACCESS_KEY)
    ttn_mqtt_client.on_connect = on_connect
    ttn_mqtt_client.on_message = on_message

    print("Connecting to Broker")
    ttn_mqtt_client.connect(TTN_BROKER_ADDRESS)

    print("Listening...")
    ttn_mqtt_client.loop_forever()

if __name__ == "__main__":
    main()
