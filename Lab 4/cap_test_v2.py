import time
import board
import busio

import adafruit_mpr121
import os

import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

import time


import digitalio
import board

from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789


import os

# For use with the STEMMA connector on QT Py RP2040
# import busio
# i2c = busio.I2C(board.SCL1, board.SDA1)
# seesaw = seesaw.Seesaw(i2c, 0x36)

seesaw = seesaw.Seesaw(board.I2C(), addr=0x36)

seesaw_product = (seesaw.get_version() >> 16) & 0xFFFF
print("Found product {}".format(seesaw_product))
if seesaw_product != 4991:
    print("Wrong firmware loaded?  Expected 4991")

seesaw.pin_mode(24, seesaw.INPUT_PULLUP)


encoder = rotaryio.IncrementalEncoder(seesaw)
last_position = None

# while True:

#     # negate the position to make clockwise rotation positive
#     position = -encoder.position

#     if position != last_position:
#         last_position = position
#         print("Position: {}".format(position))

#     if not button.value and not button_held:
#         button_held = True
#         print("Button pressed")

#     if button.value and button_held:
#         button_held = False
#         print("Button released")

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000
spi = board.SPI()
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


height = disp.width  
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)

padding = -2
top = padding
bottom = height - padding
x = 0

font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

draw.rectangle((0, 0, width, height), outline=0, fill=0)


while True:
    position = -encoder.position
    if position != last_position:
        last_position = position
        print("Position: {}".format(position))

    if position == 1:
        ma_img = Image.open("drum_title.jpg")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
    
    if position == 2:
        ma_img = Image.open("chinese_drum.jpg")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
    
    if position == 3:
        ma_img = Image.open("memes.jpg")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)

    # if not button.value and not button_held:
    #     button_held = True
    #     print("Button pressed")

    # if button.value and button_held:
    #     button_held = False
    #     print("Button released")


    for i in range(10):
        if mpr121[i].value:
            print(f"Twizzler {i} touched!")
            os.system(f'mpg321 drum{position}{i}.mp3 &')
            #time.sleep(0.25)  # Small delay to keep from spamming output messages.
