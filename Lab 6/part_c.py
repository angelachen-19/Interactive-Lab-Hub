import time
import board
import busio
import adafruit_mpr121

from i2c_button import I2C_Button

import paho.mqtt.client as mqtt
import uuid

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

topic = 'IDD/lab6/partc'

i2c = busio.I2C(board.SCL, board.SDA)

# scan the I2C bus for devices
while not i2c.try_lock():
	pass
devices = i2c.scan()
i2c.unlock()
print('I2C devices found:', [hex(n) for n in devices])
default_addr = 0x6f
if default_addr not in devices:
	print('warning: no device at the default button address', default_addr)

# initialize the button
button = I2C_Button(i2c)

button.led_bright = 50
button.led_gran = 0
button.led_cycle_ms = 0
button.led_off_ms = 0

while True:
    button.clear()
    time.sleep(1)
    if button.status.been_clicked:
        val = "i2c button clicked"
        print(val)
        client.publish(topic, val)
    
