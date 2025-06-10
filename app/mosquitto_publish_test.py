import paho.mqtt.publish as publish
from random import random


publish.single(
    "test/topic",
    random(),
    hostname="localhost",
    retain=False,
    port=1883,
    client_id="mqtt_home_utilities_publisher",
    auth={"username": "home_utilities", "password": "Z^6EGfF3g&X&qFzv"}
)
