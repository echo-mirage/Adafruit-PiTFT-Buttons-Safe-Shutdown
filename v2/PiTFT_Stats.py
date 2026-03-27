# =====================================================
# Adafruit Mini PiTFT System Stats Display v2
# =====================================================

# Script to show system stats on the Adafruit Mini PiTFT
#
# Best practice for Python 3.14 now requires scripts to be run in a virtual environment. 
# This necessitated the script to be re-worked, and it now runs as a system service.


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Import Functions
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

import time
import subprocess
import digitalio
import board
import sys
import signal

from PIL import Image, ImageDraw, ImageFont
from adafruit_rgb_display import st7789


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

time.sleep(5)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Display Configuration
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Drawing Setup
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

height = disp.width
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90
draw = ImageDraw.Draw(image)

padding = -2
top = padding
x = 0

font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24
)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Backlight
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Safe Command Execution
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode("utf-8")
    except:
        return "ERR"


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# Main Loop
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

while running:
    try:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)

        IP = "IP: " + run_cmd("hostname -I | cut -d' ' -f1")
        CPU = run_cmd("top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'")
        MemUsage = run_cmd("free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'")
        Disk = run_cmd("df -h | awk '$NF==\"/\"{printf \"Disk: %d/%d GB  %s\", $3,$2,$5}'")
        Temp = run_cmd("cat /sys/class/thermal/thermal_zone0/temp | awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'")

        y = top
        draw.text((x, y), IP, font=font, fill="#FFFFFF")
        y += font.getbbox(IP)[3]

        draw.text((x, y), CPU, font=font, fill="#FFFF00")
        y += font.getbbox(CPU)[3]

        draw.text((x, y), MemUsage, font=font, fill="#00FF00")
        y += font.getbbox(MemUsage)[3]

        draw.text((x, y), Disk, font=font, fill="#0000FF")
        y += font.getbbox(Disk)[3]

        draw.text((x, y), Temp, font=font, fill="#FF00FF")

        disp.image(image, rotation)

        time.sleep(1)

    except Exception as e:
        print(f"Stats loop error: {e}")
        time.sleep(2)

backlight.value = False
sys.exit(0)