#!/bin/bash

# Update package lists
sudo apt update

# Install python3.10-venv
sudo apt install -y python3.10-venv

# Create and activate a virtual environment
sudo python3 -m venv .
source ./bin/activate

# Install required packages
sudo apt install -y python3-pip
sudo apt install -y python3-lgpio
sudo apt-get install -y libgpiod2
sudo apt install -y python3-rpi.gpio
sudo apt install -y python3-pil

# Install Python packages using pip
sudo pip3 install influxdb
sudo python3 -m pip install simple-term-menu
sudo pip3 install adafruit-circuitpython-shtc3
sudo pip3 install sps30
sudo pip3 install smbus2
sudo pip3 install influxdb-client
sudo pip3 install python-dotenv

# Clone and install Adafruit_Python_SSD1306
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo pip3 install Adafruit_SSD1306
sudo python3 setup.py install
cd ..

# Optional: Clean up unnecessary packages to save disk space
sudo apt autoremove -y

# Optional: Deactivate the virtual environment
deactivate

echo "Setup completed!"
