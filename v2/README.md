 Adafruit Mini PiTFT Shutdown and Restart Buttons v2

![PiTFT](https://github.com/user-attachments/assets/c696ec2f-13ef-4ed8-af1c-b3999bf76faa)

Simple script to use the buttons on the Adafruit Mini PiTFT for safe shutdown and reboot, AND to display system stats on the screen.

Best practice for Python 3.14 now requires scripts to be run in a virtual environment, which broke my previous implementation of directly running the script on startup using rc.local. 
I did not write this, and the bulk of the original code belongs to Adafruit. 

The Stats script was provided via the instructions here: https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup 
You can change what's displayed by following that tutorial. Alternately, you can follow those instructions to display the console (in which case you'd use only the Buttons script provided here).

The Buttons script will make the first (top) button initiate a safe shutdown, and the second (bottom) button initiate a reboot.

I'm running these on the latest OctoPi with the Mini PiTFT: depending on your specific setup, you may need to tweak things a bit. Stats display and buttons are separated into separate scripts that are run as system services: you can use either or both scripts.

=====================================
Initial setup
=====================================

Copy PiTFT_Buttons.py and/or PiTFT_Stats.py to /home/pi/

sudo raspi-config
> Interface Options > Enable SPI

Optional: to avoid possible permission errors on /dev/spidev*, add pi to the spi and gpio groups:
sudo usermod -aG spi,gpio pi


=====================================
Set Up Python Virtual Environment
=====================================

>> Some of these commands may be redundant or unnecessary in your specific setup, but I ran them all to stamp out errors about missing packages

python3 -m venv /home/pi/PiTFT_Env

source /home/pi/PiTFT_Env/bin/activate

pip install --upgrade pip

python3 -m pip install --upgrade Pillow

pip install --upgrade spidev

pip install pillow 

pip install psutil 

pip install circup

pip install adafruit-blinka 

pip install adafruit-python-shell 

pip install adafruit-circuitpython-rgb-display 

pip install adafruit_rgb_display 

pip install adafruit-circuitpython-digitalio 

deactivate


sudo apt update

sudo apt install -y python3-dev python3-pil python3-pip python3-setuptools python3-numpy libopenjp2-7 libtiff5 libatlas-base-dev fonts-dejavu-core fonts-dejavu pillow

sudo reboot


>> Test the scripts in the virtual environment before adding them as a service

source /home/pi/PiTFT_Env/bin/activate

python /home/pi/PiTFT_Stats.py &

python /home/pi/PiTFT_Buttons.py &

>> This will run both scripts in the background until next reboot. Ensure that stats are showing on the screen and that the reboot button works. If all is well, proceed to create the services that will ensure they run with each boot with adequate permissions


=====================================
Create Buttons Service
=====================================

sudo nano /etc/systemd/system/PiTFT-buttons.service

>>>>> Paste this into PiTFT-buttons.service:
[code][Unit]
Description=PiTFT Buttons (Shutdown/Reboot)
After=multi-user.target

[Service]
Type=simple
User=root
ExecStart=/home/pi/PiTFT_Env/bin/python /home/pi/PiTFT_Buttons.py
Restart=always
RestartSec=2

[Install]
WantedBy=multi-user.target[/code]
>>>>> Write Out and Exit, saving changes


=====================================
Create Stats Service
=====================================

sudo nano /etc/systemd/system/PiTFT-stats.service

>>>>> Paste this into PiTFT-stats.service:
[code][Unit]
Description=PiTFT Stats Display
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi
ExecStartPre=/bin/sleep 5
ExecStart=/home/pi/PiTFT_Env/bin/python /home/pi/PiTFT_Stats.py
Restart=always
RestartSec=5
KillSignal=SIGTERM
KillMode=process
TimeoutStopSec=10

[Install]
WantedBy=multi-user.target[/code]
>>>>> Write Out and Exit, saving changes


===========================================================
Optional: Disable 90-second delay for OctoPrint shutdown:
===========================================================

sudo systemctl edit octoprint.service


>>>>> Paste this into octoprint.service:
[code][Service]
TimeoutStopSec=10 [/code]
>>>>> Write Out and Exit, saving changes

===========================================================
Enable Services
===========================================================

sudo systemctl daemon-reexec
sudo systemctl daemon-reload

sudo systemctl enable PiTFT-buttons.service
sudo systemctl enable PiTFT-stats.service

sudo systemctl start PiTFT-buttons.service
sudo systemctl start PiTFT-stats.service



===========================================================
If you need to test or see live logs:
===========================================================

sudo systemctl status PiTFT-buttons.service
sudo systemctl status PiTFT-stats.service

journalctl -u PiTFT-buttons.service -f
journalctl -u PiTFT-stats.service -f
