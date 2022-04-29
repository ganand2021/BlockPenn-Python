# BlockPenn-Python
Python code for the RPi sensors.

## Installation
1. Complete deploying the docker image of blockpenn on the RPi. 
2. Follow the steps to set up for `sensor_start_w_sps`
3. Set up crontab to auto start the script in reboot

### sensor_start_w_sps
This is the Python code with all sensors (Air quality, CO2, Humidity & Temp) and OLED display.

#### Setting up the environment (Script)
```sh
sudo sh setup_pkg.sh
sh setup_env.sh
```

#### Setting up the environment (Manual)
General:
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
sudo pip3 install sps30
sudo pip3 install smbus2
```

### Set up crontab to auto start the script in reboot
Open crontab:
```sh
sudo crontab -e
```
Pick your preferred editor and add the following line to the crontab file:
```
@reboot sh /home/ubuntu/blockpenn-python/run_sensor_script.sh >> /var/log/sensor_script.log 2>&1
```

Test by rebooting.

## Open items
- [x] OLED support
- [x] SHTC3 support
- [x] T6713 support
- [x] Create main script
- [x] Rotate the display between panels
- [x] Check the readings from the CO2 sensor (return the full buffer to see it's correct)
- [x] Validate CO2 readings: the sensor readings and reset doesn't make sense
- [x] Consider decreasing T6713 delays (can be 10 miliseconds per application notes)
- [x] Read directly from I2C for SHTC3
- [x] Add air quality sensor
- [x] Add integration with Kasa API
- [x] Add logging to sensor_start
- [x] Limit log size / rotate files
- [x] Switch to GPIO
- [x] Re-enable SPS30
- [x] Add a script for auto restarting the python code in case of crash
- [x] Add autostart in reboot instructions 
- Features:
- [x] Write sensor data to InfluxDB
- Environment/setup:
- [ ] Add VENV
- [ ] Create requirements.txt
- Functionality:
- [ ] Seperate the sampling into its own function in the sensor_start
- [x] Connect controls: button
- [x] Connect controls: leds
- [x] Add functionality to buttons via events
- [x] Add blinking ok led
- [ ] Add plug load monitoring to the script

## Future features
`pip3 install -r requirements.txt`

## Links
- Useful I2C commands: https://www.waveshare.com/wiki/Raspberry_Pi_Tutorial_Series:_I2C
- T6713 datasheet: http://www.co2meters.com/Documentation/Datasheets/DS-AMP-0002-T6713-Sensor.pdf
- T6713 application notes: https://f.hubspotusercontent40.net/hubfs/9035299/Documents/AAS-916-142A-Telaire-T67xx-CO2-Sensor-022719-web.pdf
- T6713 digikey page: https://www.digikey.com/en/products/detail/amphenol-advanced-sensors/T6713/5027891
- I2C UM10204: https://www.nxp.com/docs/en/user-guide/UM10204.pdf
- Connectd guide to reading SHTC3: https://blog.dbrgn.ch/2018/8/20/read-shtc3-sensor-from-linux-raspberry-pi/
- Python Kasa: https://python-kasa.readthedocs.io/en/latest/smartplug.html
- SPS30 datasheet: https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/9.6_Particulate_Matter/Datasheets/Sensirion_PM_Sensors_Datasheet_SPS30.pdf
- SPS30 page: https://www.sensirion.com/en/environmental-sensors/particulate-matter-sensors-pm25/

## Side notes
- Consider using `sensors` (`sudo apt install lm-sensors`) to check the internal temperature
- Create the requirements.txt: `pip3 freeze > requirements.txt`
- Good diagram of particles types (p. 13): https://cdn-learn.adafruit.com/downloads/pdf/pm25-air-quality-sensor.pdf

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

