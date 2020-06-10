from mqttsn.client import Client, Callback

import sys


class MyCallback(Callback):
    def message_arrived(self, topic_name, payload, qos, retained, msgid):
        print(f'{self} | topic_name: {topic_name} | payload: {payload} | '
              f'qos {qos} | retained {retained} | msgid {msgid}',
              file=sys.stderr)

        return True

def main():
    aclient = Client("bridge", port=1885)
    aclient.register_callback(MyCallback())
    aclient.connect()

    rc, sensor_topic = aclient.subscribe("sensor_values")

    aclient.start_receiver()

if __name__ == "__main__":
    main()