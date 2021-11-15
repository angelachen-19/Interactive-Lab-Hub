import time
import enum
import signal
import board
import busio
import adafruit_mpr121
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

import paho.mqtt.client as mqtt
import uuid

from subprocess import call

topic_prefix = 'IDD/lab6_part_e/'

### Publisher Section ###

publisher_topic = topic_prefix + 'publisher/speak'

def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(publisher_topic)

def on_message(cleint, userdata, msg):
    # if a message is recieved on the colors topic, parse it and set the color
    if msg.topic == publisher_topic:
        wrods = str(msg.payload.decode('UTF-8'))
        print(msg.topic+" "+wrods)
        command = """
            say() { 
                local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; 
            } ; 
        """ + f"say '{wrods}'"
        call(command, shell=True)

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message

client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

client.loop_start()

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)

# hen sigint happens, do the handler callback function
signal.signal(signal.SIGINT, handler)

### Feedback Section ###

name = "test0"

feedback_topic = topic_prefix + 'feedback/' + name

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

# Enum class for feedback, used to convert mpr121 output 
class Feedback(enum.Enum):
    waking_up = 11
    others = 5
    no_response = -1
    five_more_minutes = 6
    not_getting_up = 0

    @classmethod
    def _missing_(cls, value):
        return Feedback.others

# dictionary to convert Feedback to string
feedback_to_string = {
    Feedback.waking_up: "I am waking up",
    Feedback.others: "did not recognize the response",
    Feedback.no_response: "no response",
    Feedback.five_more_minutes: "five more minutes",
    Feedback.not_getting_up: "I am not getting up today"
}

### Display Section ###

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

### Main Loop ###

current_response = feedback_to_string[Feedback.no_response]
client.publish(feedback_topic, current_response)

# keep track of the no_reponse time, when the threshold is reached, change the 
# current_response to no_reponse
no_response_counter = 0
no_response_threshold = 5

loop_sleeping_time = 0.5

while True:
    for i in range(12):
        if mpr121[i].value:
            # print(f"Twizzler {i} touched!")
            current_response = feedback_to_string[Feedback(i)]
            print(current_response)
            client.publish(feedback_topic, current_response)
            no_response_counter = 0
            break

    # check if the threshold is reached
    if no_response_counter > no_response_threshold:
        current_response = feedback_to_string[Feedback.no_response]
        client.publish(feedback_topic, current_response)
        no_response_counter = 0

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    time_string = time.strftime("%H:%M:%S")
    dx, dy = font.getsize(time_string)
    x = (width - dx) / 2
    y = (height - dy) / 2
    draw.text((x, y), time_string, font=font, fill="#FFFFFF")

    disp.image(image, rotation)

    time.sleep(loop_sleeping_time)

    # increment the counter
    no_response_counter += loop_sleeping_time
