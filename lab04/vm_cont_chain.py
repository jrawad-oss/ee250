import paho.mqtt.client as mqtt
import time

rpi_broker = "172.20.10.3"
port = 1883

def on_message(client, userdata, msg):
    num = int(msg.payload.decode())

    num += 1
    time.sleep(1)

    client.publish("jrawad/pong", num)
    print("msg: ", num)

client = mqtt.Client()
client.on_message = on_message
client.connect(rpi_broker, port)
client.subscribe("jrawad/ping")

client.loop_forever()

