#!/bin/bash

echo "Setting up the environment for the project"

python3 -m venv .
source ./venv/bin/activate
pip3 install influxdb
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
pip3 install Adafruit_Python_SSD1306
python3 setup.py install
cd ..
pip3 install adafruit-circuitpython-shtc3
