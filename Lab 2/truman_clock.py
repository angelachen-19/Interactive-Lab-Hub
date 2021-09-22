# import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
# from time import strftime, sleep
from adafruit_rgb_display.rgb import color565
from datetime import datetime, time
from time import sleep

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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# these setup the code for our buttons 
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# ----

fake_time = datetime.now()

# Helper Functions: 
def clear_image():
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

def isPressed_A():
    return not buttonA.value

def isPressed_B():
    return not buttonB.value

def draw_text_align(min_x, min_y, max_x, max_y, msg, font=font, fill="#FFFFFF"):
    # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    w, h = draw.textsize(msg, font=font)
    draw.text((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2), msg, font=font, fill=fill)
    # print((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2))

def draw_text_align(msg, font=font, fill="#FFFFFF"):
    # font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    min_x, min_y, max_x, max_y = Display.x0, Display.y0, Display.x1, Display.y1
    w, h = draw.textsize(msg, font=font)
    draw.text((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2), msg, font=font, fill=fill)
    # print((min_x+(max_x-min_x-w)/2,min_y+(max_y-min_y-h)/2))


# Classes
class Interaction:
    Default = 0
    A = 1 # Button A
    B = 2 # Button B
    AnB = 3 # Button A & B

class TimeSlot:
    color = "White"
    title = "Truman Clock"
    greeting = "Hi Truman"
    start_time = 0
    end_time = 100
    word_color = "White"
    background_color = "Black"

    def __init__ (self):
        return

    def in_range(self, in_time):
        # if in range
        if self.start_time <= self.end_time:
            return self.start_time <= in_time < self.end_time
        return self.start_time <= in_time or in_time < self.end_time

    def show_greeting(self):
        draw_text_align(self.greeting)

    def get_width(self, in_time):
        def get_min(date_time):
            total_min = date_time.hour * 60 + date_time.minute
            return total_min

        # Get the length of pixel 
        total_min = in_time.hour * 60 + in_time.minute
        print(total_min)

        in_min = get_min(in_time)
        start_min = get_min(self.start_time)
        end_min = get_min(self.end_time)

        if start_min < in_min: 
            w = 240 * (end_min - in_min) / (end_min - start_min)
        elif in_min < end_min: 
            w = 240 * (end_min - in_min) / (end_min + 1440 - start_min)

        print(get_min(self.start_time))
        # w = 240 * (total_min - self.start_time) / (self.end_time - self.start_time)
        return w

    def show_background(self, in_time):
        w = self.get_width(in_time)
        print("W" , w)
        draw.rectangle((0, 0, w, 135), outline=0, fill=self.color)

    def show(self, in_time):
        clear_image()
        self.show_background(in_time)
        self.show_greeting()

        # Display Text
        

# Morning
MORNING = TimeSlot()
MORNING.color = "#98DB8D"
MORNING.title = "morning"
MORNING.greeting = "Good Morning!"
MORNING.start_time = time(6, 0)
MORNING.end_time = time(12, 0)

# Afternoon
AFTERNOON = TimeSlot()
AFTERNOON.color = "#FFC061"
AFTERNOON.title = "afternoon"
AFTERNOON.greeting = "Good Afternoon!"
AFTERNOON.start_time = time(12, 0)
AFTERNOON.end_time = time(18, 0)

# Evening
EVENING = TimeSlot()
EVENING.color = "#4F8AFF"
EVENING.title = "evening"
EVENING.greeting = "Good Evening!"
EVENING.start_time = time(18, 0)
EVENING.end_time = time(0, 0)

# Night
NIGHT = TimeSlot()
NIGHT.color = "#8254BD"
NIGHT.title = "night"
NIGHT.greeting = "Good Night!"
NIGHT.start_time = time(0, 0)
NIGHT.end_time = time(6, 0)

VOIDTIME = TimeSlot()

# Default Settings
TIME_SLOTS = [MORNING, AFTERNOON, EVENING, NIGHT]

class Display:
    """
               Adafruit   miniPiTFT 1.14"   240x135

            (x0, y1) ------------------------ (x1, y1)
                |                                 |
    [Button_A]  |                                 |
                |                                 |
                |                                 |
    [Button_B]  |                                 |
                |                                 |
            (x0, y0) ------------------------ (x1, y0)

    """
    x0, x1 = 0, 240
    y0, y1 = 0, 135

def get_current_slot(in_time):
    for t in TIME_SLOTS:
        if t.in_range(in_time):
            return t
    return VOIDTIME

# Run it!
while True:
    # Draw a black filled box to clear the image.
    # clear_image()
    real_time = datetime.now().time()
    curr_slot = get_current_slot(real_time)

    # Get Current Timeslot 
    curr_slot.show(real_time);
    # Display image.
    disp.image(image, rotation)
    sleep(30)




    