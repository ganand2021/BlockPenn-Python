# BlockPenn-Python
Python code for the RPi sensors

## How to run
### sensor_start
`sensor_start.py`: this is the I2C code with all 2 sensors (CO2, Humidity & Temp) and OLED display.
#### Setting up the environment
```sh
git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
sudo python3 setup.py install
cd examples
sudo apt install -y python3-pil
sudo apt install -y python3-rpi.gpio
git clone https://github.com/adafruit/Adafruit_CircuitPython_SHTC3
cd Adafruit_CircuitPython_SHTC3
sudo pip3 install adafruit-circuitpython-shtc3
sudo python3 setup.py install
```
### sensor_set
`sensor_set.py`: this is the I2C code without the OLED display, but it doesn't require any additional packages.

# VENV
Set up venv:
`python3 -m venv .`
Activate venv:
`source ./bin/activate`
Deactivate venv:
`deactivate`

### Main script
Run `sensor_start.py`

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
- [x] Add logging to sensor_start
- [ ] Add logging to sensor_set
- [ ] Limit log size / rotate files
- [ ] Add VENV
- [ ] Create requirements.txt
- [ ] Write sensor data to InfluxDB
- [ ] Connect controls: button
- [ ] Connect controls: leds
- [ ] Add plug load monitoring
- [ ] Add case
- [ ] Add air quality sensor
- [ ] Add integration with Kasa API

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

## Side notes
- Consider using `sensors` (`sudo apt install lm-sensors`) to check the internal temperature
- Create the requirements.txt: `pip3 freeze > requirements.txt`