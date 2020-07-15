import ssl

BROKERADDRESS = "<aws-iot-device-address>.iot.us-east-1.amazonaws.com"
BROKERPORT = 8883
CA_CERTIFICATE = "../aws/AmazonRootCA1.pem"
CLIENT_CERTIFICATE = "../aws/certificate.pem.crt"
PRIVATE_KEY = "../aws/private.pem.key"

IoT_protocol_name = "x-amzn-mqtt-ca"
aws_iot_endpoint = BROKERADDRESS # <random>.iot.<region>.amazonaws.com
url = "https://{}".format(aws_iot_endpoint)

def ssl_alpn():
    try:
        #debug print opnessl version
        #logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=CA_CERTIFICATE)
        ssl_context.load_cert_chain(certfile=CLIENT_CERTIFICATE, keyfile=PRIVATE_KEY)
        return ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e