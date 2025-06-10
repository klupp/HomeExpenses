from paho.mqtt.subscribe import simple

val = simple(
    "test/topic",
    msg_count=5,
    retained=True,
    hostname="localhost",
    port=1883,
    client_id="mqtt_home_utilities_simple_subscriber",
    auth={"username": "home_utilities", "password": "Z^6EGfF3g&X&qFzv"}
)

print(val)