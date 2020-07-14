import json
import boto3
import math

print('Loading function')


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    client = boto3.client('iot-data', region_name='us-east-1')

    if "x" in event and "y" in event and "z" in event:
        x = float(event["x"])
        y = float(event["y"])
        z = float(event["z"])
        module = math.sqrt(math.pow(x, 2) + math.pow(x, 2) + math.pow(x, 2))
        if module > 2:
            state = "RUNNING"
        elif module > 0.5:
            state = "WALKING"
        else:
            state = "STANDING"
        event["state"] = state

        print(event)

    # Change topic, qos and payload
    response = client.publish(
        topic='stations/mobile_sensor_states',
        qos=1,
        payload=json.dumps(event)
    )
    return response
