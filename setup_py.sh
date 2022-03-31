#!/bin/bash

echo "Setting up RPi Python scripts environment for the first time"

read -p "Password: " -s szPassword
printf "%s\n" "$szPassword" | sudo --stdin mount -t cifs //192.168.1.1/home /media/$USER/home -o username=$USER,password="$szPassword"

sudo -u ubuntu apt install python3-pip
sudo -u ubuntu apt install python3-lgpio
sudo -u ubuntu apt-get install libgpiod2
sudo -u ubuntu apt install -y python3-rpi.gpio
sudo -u ubuntu apt install -y python3-pil

python3 -m venv .
source ./venv/bin/activate
pip3 install influxdb
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
pip3 install Adafruit_Python_SSD1306
python3 setup.py install
cd ..
pip3 install adafruit-circuitpython-shtc3
