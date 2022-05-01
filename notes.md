# Side notes
This is a general "catch all" I created for the development notes that didn't fit anywhere else. 

## Other scripts
### sensor_start_no_sps
`sensor_start_no_sps.py`: this is the I2C code with the CO2, Humidity & Temp sensors and OLED display.
#### Setting up the environment
```sh
sudo python3 -m venv .
source ./bin/activate
sudo apt install python3-pip
sudo pip3 install influxdb
sudo apt install python3-lgpio
sudo apt-get install libgpiod2
sudo apt install -y python3-rpi.gpio
sudo apt install -y python3-pil
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo pip3 install Adafruit_Python_SSD1306
sudo python3 setup.py install
cd ..
sudo pip3 install adafruit-circuitpython-shtc3
```

### sensor_set
`sensor_set.py`: this is the I2C code without the OLED display, but it doesn't require any additional packages.

## Setting up specific libraries
Adafruit_Python_SSD1306:
```sh
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
sudo python3 setup.py install
cd examples
sudo apt install -y python3-pil
sudo apt install -y python3-rpi.gpio
```
Adafruit_CircuitPython_SHTC3:
```sh
git clone https://github.com/adafruit/Adafruit_CircuitPython_SHTC3
cd Adafruit_CircuitPython_SHTC3
sudo pip3 install adafruit-circuitpython-shtc3
sudo python3 setup.py install
```
SPS30
```sh
pip3 install sps30
```

## VENV
Set up venv:
`python3 -m venv .`
Activate venv:
`source ./bin/activate`
Deactivate venv:
`deactivate`