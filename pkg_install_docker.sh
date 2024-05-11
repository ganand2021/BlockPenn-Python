#!/bin/bash
#Change Working Directory
cd ..

# Ensure the script is run as root without needing 'sudo'
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

# Update and upgrade the system
apt-get update && apt-get upgrade -y

# Install required packages
apt-get install -y net-tools i2c-tools python3-pip python3-lgpio libgpiod2 python3-rpi.gpio python3-pil

pip3 install virtualenv

# Assuming python3.10 is available and correct
# If python3.10-venv was successfully installed, python3 should be recognized.
# Set up a virtual environment. Ensure python3.10-venv is installed or use the appropriate version
virtualenv bpenv

# Activate the virtual environment
source bpenv/bin/activate

# Install python packages. Use 'pip' instead of 'pip3' as we are inside the virtual environment
pip install simple-term-menu adafruit-circuitpython-shtc3 sps30 smbus2 awsiotsdk awscrt RPi.GPIO Pillow Adafruit_SSD1306 requests python-dotenv

# Deactivate the virtual environment when done
deactivate

echo "Installation complete!"