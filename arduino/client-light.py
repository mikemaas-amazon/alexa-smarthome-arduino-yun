import json
import sys
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Include the Arduino BridgeClient
sys.path.insert(0, '/usr/lib/python2.7/bridge')
from bridgeclient import BridgeClient

# !!! Configuration settings !!!
# You will need to change these reflect your AWS IoT configuration
thing_name = 'arduino-sample'
thing_endpoint = 'a311mxzpj0i4v.iot.us-east-1.amazonaws.com'
thing_aws_root_cert = 'aws-iot-rootCA.crt'  # Something like aws-iot-rootCA.crt
thing_private_key = 'arduino-test.private.key'  # Something like arduino-test.private.key
thing_cert = 'arduino-test.cert.pem'  # Something like arduino-test.cert.pem


def custom_callback_accepted(client, userdata, message):
    """
    Callback to handle passing a custom message to the other processor via the bridge
    """
    print('Callback', message.payload)
    msg = json.loads(message.payload)

    brightness = msg['state']['desired']['brightness']
    color = msg['state']['desired']['color']
    power = msg['state']['desired']['power']

    code = 'NOOP'
    if brightness != '*':
        code = 'B' + str(brightness)

    if color != '*':
        code = 'C' + color

    if power != '*':
        code = 'P' + power

    client = BridgeClient()
    client.mailbox(code)
    print("Sent Message:", code)


def main():
    """
    Main function that spins up an MQTT client and listens for our custom messages
    """
    print('Initializing')
    client = AWSIoTMQTTClient("sub-arduino-client-id")
    client.configureEndpoint(thing_endpoint, 8883)
    client.configureCredentials(thing_aws_root_cert, thing_private_key, thing_cert)
    client.configureConnectDisconnectTimeout(10)
    client.configureMQTTOperationTimeout(5)

    print('Connecting')
    client.connect()
    # Subscribe to accepted updates and call our message callback when a custom message is found
    client.subscribe('$aws/things/' + thing_name + '/shadow/update/accepted', 1, custom_callback_accepted)

    while True:
        time.sleep(10)
        print('.')


if __name__ == '__main__':
    main()
