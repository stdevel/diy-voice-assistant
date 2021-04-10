#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Listens for Rhasspy events and animates pixel ring accordingly
"""

import logging
import argparse
from paho.mqtt import client as mqtt_client
from gpiozero import LED
from pixel_ring import pixel_ring

LOGGER = logging.getLogger('lights')
"""
logging: Logger instance
"""
LOG_LEVEL = None
"""
logging: Logger level
"""
FILE_PATH = "/tmp"
"""
str: path to write files to
"""


def parse_options():
    """Parses options and arguments."""
    desc = '''%(prog)s is used for subscribing to MQTT topics
    and write them to a file.'''
    epilog = '''Check-out the website for more details:
     https://github.com/stdevel/diy-voice-assistant'''
    parser = argparse.ArgumentParser(
        description=desc, epilog=epilog
    )

    # define option groups
    gen_opts = parser.add_argument_group("generic arguments")
    led_opts = parser.add_argument_group("LED arguments")
    mqtt_opts = parser.add_argument_group("MQTT arguments")

    # GENERIC ARGUMENTS
    # -d / --debug
    gen_opts.add_argument(
        "-d", "--debug",
        dest="generic_debug",
        default=False,
        action="store_true",
        help="enable debugging outputs (default: no)"
    )

    # LED ARGUMENTS
    # -b / --brightness
    led_opts.add_argument(
        "-b", "--brightness",
        dest="led_brightness",
        metavar="INT",
        default=10,
        action="store",
        type=int,
        help="sets brightness level (default: 10)"
    )
    # --pattern
    led_opts.add_argument(
        "--pattern",
        dest="led_pattern",
        default="google",
        choices=['echo', 'google'],
        action="store",
        type=str,
        help="sets animation pattern (default: google)"
    )

    # MQTT ARGUMENTS
    # -H / --host
    mqtt_opts.add_argument(
        "-H", "--host",
        dest="mqtt_host",
        metavar="HOSTNAME",
        default="localhost",
        action="store",
        type=str,
        help="sets MQTT broker (default: localhost)"
    )
    # -P / --port
    mqtt_opts.add_argument(
        "-P", "--port",
        dest="mqtt_port",
        metavar="PORT",
        default=12183,
        action="store",
        type=int,
        help="sets MQTT port (default: 12183)"
    )
    # -u / --username
    mqtt_opts.add_argument(
        "-u", "--username",
        dest="mqtt_username",
        metavar="USERNAME",
        default=None,
        action="store",
        type=str,
        help="sets MQTT user (default: empty)"
    )
    # -p / --password
    mqtt_opts.add_argument(
        "-p", "--password",
        dest="mqtt_password",
        metavar="PASSWORD",
        default=None,
        action="store",
        type=str,
        help="sets MQTT password (default: empty)"
    )

    # parse options and arguments
    return parser.parse_args()


def connect_mqtt(username, password, hostname, port) -> mqtt_client:
    """
    Connect to MQTT broker
    """
    client_id = "rhasspy_lights"

    def on_disconnect(client, userdata, return_code):
        LOGGER.error("Connection to MQTT broker lost")

    def on_connect(client, userdata, flags, return_code):
        if return_code == 0:
            LOGGER.info("Connected to MQTT Broker!")
        else:
            LOGGER.error("Failed to connect, return code %d\n", return_code)
    # set Connecting Client ID
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(hostname, port)
    return client


def subscribe(client: mqtt_client, topics):
    """
    This function subscribes to a MQTT topic
    """
    def on_connect(client, userdata, flags, return_code):
        if return_code == 0:
            LOGGER.info("Connected to MQTT Broker and subscribed topics")
            # subscribe to topics again
            client.subscribe(topics)
        else:
            LOGGER.error("Failed to connect, return code %d\n", return_code)

    def on_disconnect(client, userdata, return_code):
        LOGGER.info("Subscription lost")

    def on_message(client, userdata, msg):
        LOGGER.debug(
            "Received '%s' from '%s' topic",
            msg.payload.decode(), msg.topic
            )
        if "sessionStarted" in msg.topic:
            # listening
            LOGGER.debug("Light waking up")
            pixel_ring.wakeup()
        elif "stopListening" in msg.topic:
            # processing
            LOGGER.debug("Light processing...")
            pixel_ring.think()
        elif "intentParsed" in msg.topic:
            # command detected
            LOGGER.debug("Light speaking...")
            pixel_ring.speak()
        elif "sessionEnded" in msg.topic:
            # stop flashing
            LOGGER.debug("Light turning off...")
            pixel_ring.off()
    # add callback
    client.subscribe(topics)
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect


def start_subscribe(options):
    """
    Subscribe all the topics
    """
    # create tuple configuration
    topics = [
        ('hermes/dialogueManager/sessionStarted', 0),
        ('hermes/nlu/intentParsed', 0),
        ('hermes/dialogueManager/sessionEnded', 0)
    ]
    # connect to MQTT
    client = connect_mqtt(
        options.mqtt_username,
        options.mqtt_password,
        options.mqtt_host,
        options.mqtt_port
        )
    subscribe(client, topics)
    client.loop_forever()


def main(options):
    """
    Main function, starts the logic based on parameters.
    """
    LOGGER.debug("Options: %s", options)
    # start LED ring
    power = LED(5)
    power.on()
    pixel_ring.set_brightness(options.led_brightness)
    pixel_ring.change_pattern(options.led_pattern)
    # subscribe topics
    start_subscribe(options)


def cli():
    """
    This functions initializes the CLI interface
    """
    # global LOG_LEVEL
    options = parse_options()

    # set logging level
    logging.basicConfig()
    if options.generic_debug:
        LOG_LEVEL = logging.DEBUG
    else:
        LOG_LEVEL = logging.INFO
    LOGGER.setLevel(LOG_LEVEL)

    main(options)


if __name__ == "__main__":
    cli()
