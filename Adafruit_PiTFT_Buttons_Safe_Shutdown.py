# ==================================================
#  Adafruit Mini PiTFT Shutdown and Restart Buttons
# ==================================================
# This is a simple python script to use the buttons on the Adafruit Mini PiTFT screen to initiate a safe shutdown and a safe reboot. 
#
# I am not the author, that credit goes to mikeysklar on the Adafruit forums.
#
# You'll need to follow the instructions on Adafruit's site for installing and setting up the Python display libraries
# https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup
#
# 
# This was set up on a Pi Zero 2W. Depending on which version of the Pi you're using, you'll probably need to change the appropriate sections below in your config.
#
# Following the setup instructions, the script is called stats.py
# Set it to run on boot by placing it in /etc/rc.local
# Then run sudo nano /etc/rc.local, and on its own line before exit 0 add the line 
# sudo python3 /home/pi/stats.py &

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import digitalio
import board
import os
import time

from adafruit_rgb_display import st7789

# Configuration for CS and DC pins for Raspberry Pi
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000

# Create the ST7789 display:
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Initialize buttons
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Initialize backlight control on D22
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True  # Turn on backlight by default

# Functions
def shutdown_system():
    print("Shutting down...")
    backlight.value = False  # Turn off the backlight
    os.system("sudo shutdown -h now")  # Execute shutdown command

def reboot_system():
    print("Rebooting...")
    os.system("sudo reboot")  # Execute reboot command

# Main loop:
while True:
    # Button Press Logic
    if not buttonA.value and buttonB.value:  # Just Button A pressed
        shutdown_system()  # Shutdown when Button A is pressed

    elif not buttonB.value and buttonA.value:  # Just Button B pressed
        reboot_system()  # Reboot when Button B is pressed

    # Optional: Add a short delay to debounce buttons
    time.sleep(0.1)