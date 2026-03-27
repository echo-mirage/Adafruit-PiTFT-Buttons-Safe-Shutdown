 Adafruit Mini PiTFT Shutdown and Restart Buttons

![PiTFT](https://github.com/user-attachments/assets/c696ec2f-13ef-4ed8-af1c-b3999bf76faa)

This is a simple python script to use the buttons on the Adafruit Mini PiTFT screen to initiate a safe shutdown and a safe reboot. 

I am not the author, that credit goes to mikeysklar on the Adafruit forums.

You'll need to follow the instructions on Adafruit's site for installing and setting up the Python display libraries
https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-setup


This was set up on a Pi Zero 2W. Depending on which version of the Pi you're using, you'll probably need to change the appropriate sections below in your config.

Following the setup instructions, the script is called stats.py
Set it to run on boot by placing it in /etc/rc.local
Then run sudo nano /etc/rc.local, and on its own line before exit 0 add the line 
sudo python3 /home/pi/stats.py &
