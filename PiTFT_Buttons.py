
# =====================================================
# Adafruit Mini PiTFT Shutdown and Restart Buttons v2
# =====================================================

# Script to use the hardware buttons on the Adafruit Mini PiTFT to initiate safe shutdown and reboot.
#
# Best practice for Python 3.14 now requires scripts to be run in a virtual environment. 
# This necessitated the script to be re-worked, and it now runs as a system service.


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Import Functions
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import time
import digitalio
import board
import os
import signal
import sys


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Shutdown handling
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

running = True

def handle_exit(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Startup delay
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

time.sleep(2)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Buttons
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)

buttonA.switch_to_input(pull=digitalio.Pull.UP)
buttonB.switch_to_input(pull=digitalio.Pull.UP)

# Debounce
last_button_time = 0
DEBOUNCE_DELAY = 0.3


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Functions
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def shutdown_system():
    print("Shutting down...")
    os.system("shutdown -h now")

def reboot_system():
    print("Rebooting...")
    os.system("reboot")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Main Loop
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

while running:
    try:
        current_time = time.time()

        if current_time - last_button_time > DEBOUNCE_DELAY:
            if not buttonA.value and buttonB.value:
                last_button_time = current_time
                shutdown_system()

            elif not buttonB.value and buttonA.value:
                last_button_time = current_time
                reboot_system()

        time.sleep(0.05)

    except Exception as e:
        print(f"Button loop error: {e}")
        time.sleep(1)

sys.exit(0)