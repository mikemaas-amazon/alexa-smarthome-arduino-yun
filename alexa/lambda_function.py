import boto3
import colorsys
import json
import time
import uuid

from color_tools import convert_K_to_RGB

aws_iot = boto3.client('iot-data')

# The name of our light as set in AWS IoT
thing_name = 'arduino-test'

# Our custom message template for sending messages to the Arduino via MQTT
msg_template = {
    'state': {
        'desired':
            {
                'brightness': '0',
                'color': '0|0|0|',
                'power': '*'
            }
    }
}


def get_utc_timestamp(seconds=None):
    """
    Helper function for generating a UTC timestamp
    :param seconds: Seconds since the Epoch or current time if None.
    :return: A time UTC timestamp string
    """
    return time.strftime('%Y-%m-%dT%H:%M:%S.00Z', time.gmtime(seconds))


def set_brightness(value, is_delta):
    """
    Send a brightness value to the light Thing shadow
    :param value: The brightness value
    :param is_delta: The value is a percentage adjustment to the current value
    """

    # Get a copy of our message template
    msg = msg_template.copy()

    brightness_value = value
    if is_delta:
        b_value = int(brightness_value)
        if b_value == 0:
            brightness_value = '*'
        elif b_value < 0:
            brightness_value = str(brightness_value)
        else:
            brightness_value = '+' + str(brightness_value)

    msg['state']['desired']['brightness'] = brightness_value
    msg['state']['desired']['color'] = '*'
    msg['state']['desired']['power'] = '*'
    mqtt_msg = json.dumps(msg)

    response = aws_iot.update_thing_shadow(thingName=thing_name, payload=mqtt_msg.encode())

    # Debug - This will dump to CloudWatch
    print(response)


def set_color(value, is_kelvin=False):
    """
    Send a color value to the light Thing shadow
    :param value: The color value in Kelvin or HSV
    :param is_kelvin: Convert the value as Kelvin
    """

    # Get a copy of our message template
    msg = msg_template.copy()

    r = g = b = 0

    if is_kelvin:
        color = convert_K_to_RGB(value)
        r = int(color[0])
        g = int(color[1])
        b = int(color[2])
    else:
        hue_value = value / 360
        color = colorsys.hsv_to_rgb(hue_value, 1.0, 1.0)
        r = int(color[0] * 255)
        g = int(color[1] * 255)
        b = int(color[2] * 255)

    color_string = '{0}|{1}|{2}|'.format(r, g, b)
    msg['state']['desired']['brightness'] = '*'
    msg['state']['desired']['color'] = color_string
    msg['state']['desired']['power'] = '*'
    mqtt_msg = json.dumps(msg)

    response = aws_iot.update_thing_shadow(thingName=thing_name, payload=mqtt_msg.encode())

    # Debug - This will dump to CloudWatch
    print(response)


def turn_on(value=False):
    """
    Send an On or Off command to the light Thing shadow
    :param value: Boolean to indicate whether to turn on
    """
    # Get a copy of our message template
    msg = msg_template.copy()

    state_value = 'OFF'
    if value:
        state_value = 'ON'
    msg['state']['desired']['brightness'] = '*'
    msg['state']['desired']['color'] = '*'
    msg['state']['desired']['power'] = state_value
    mqtt_msg = json.dumps(msg)

    response = aws_iot.update_thing_shadow(thingName=thing_name, payload=mqtt_msg.encode())

    # Debug - This will dump to CloudWatch
    print(response)


def handler(request, context):
    """
    Handle incoming Alexa directives
    :param request: Directive request for the Lambda handler
    :param context: Context for the request
    :return:
    """

    try:
        # Debug - This will dump to CloudWatch
        print("Directive:", request)
        response = '{}'

        request_namespace = request['directive']['header']['namespace']

        if request_namespace == "Alexa.Authorization":
            # HACK Blindly responding OK to an Authorization request - Set up your own auth as appropriate
            response_file = open('response-event-authorization.json', 'r')
            response = json.load(response_file)

        if request_namespace == 'Alexa.BrightnessController':
            request_name = request['directive']['header']['name']
            correlation_token = request['directive']['header']['correlationToken']
            endpoint_id = request['directive']['endpoint']['endpointId']
            token = request['directive']['endpoint']['scope']['token']

            brightness = 0
            if request_name == 'AdjustBrightness':
                brightness = request['directive']['payload']['brightnessDelta']
                set_brightness(brightness, is_delta=True)

            if request_name == 'SetBrightness':
                brightness = request['directive']['payload']['brightness']
                set_brightness(brightness, is_delta=False)

            response_file = open('response-context-event.json', 'r')
            response = json.load(response_file)
            response['context']['properties'][0]['namespace'] = request_namespace
            response['context']['properties'][0]['name'] = 'brightness'
            # NOTE We are not storing the current brightness value here so delta adjustments will be inaccurate
            response['context']['properties'][0]['value'] = abs(brightness)
            response['context']['properties'][0]['timeOfSample'] = get_utc_timestamp()
            response['context']['properties'][0]['uncertaintyInMilliseconds'] = 1000
            response['event']['header']['messageId'] = str(uuid.uuid4())
            response['event']['header']['correlationToken'] = correlation_token
            response['event']['endpoint']['scope']['token'] = token
            response['event']['endpoint']['endpointId'] = endpoint_id

        if request_namespace == "Alexa.ColorController":
            correlation_token = request['directive']['header']['correlationToken']
            token = request['directive']['endpoint']['scope']['token']

            response_file = open('response-event-color-set.json', 'r')
            response = json.load(response_file)
            response['event']['header']['correlationToken'] = correlation_token
            response['event']['endpoint']['scope']['token'] = token
            hue = request['directive']['payload']['color']['hue']  # Handling the SetColor directive

            set_color(hue)

        if request_namespace == "Alexa.ColorTemperatureController":
            correlation_token = request['directive']['header']['correlationToken']
            token = request['directive']['endpoint']['scope']['token']
            kelvin = request['directive']['payload']['colorTemperatureInKelvin']

            response_file = open('response-event-color-temp.json', 'r')
            response = json.load(response_file)
            response['context']['properties'][0]['value'] = kelvin
            response['event']['header']['correlationToken'] = correlation_token
            response['event']['endpoint']['scope']['token'] = token

            set_color(kelvin, is_kelvin=True)

        if request_namespace == "Alexa.Discovery":
            response_file = open('response-event-discovery.json', 'r')
            response = json.load(response_file)

        if request_namespace == "Alexa.PowerController":
            request_name = request['directive']['header']['name']
            correlation_token = request['directive']['header']['correlationToken']
            token = request['directive']['endpoint']['scope']['token']

            response_file = open('response-event-power.json', 'r')
            response = json.load(response_file)
            response['event']['header']['correlationToken'] = correlation_token
            response['event']['endpoint']['scope']['token'] = token
            if request_name == 'TurnOff':
                response['context']['properties'][0]['value'] = 'OFF'
                turn_on(False)
            else:
                response['context']['properties'][0]['value'] = 'ON'
                turn_on(True)

        print('Event:', response)
        return response

    except ValueError as error:
        print(error)
        raise
