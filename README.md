# BlockPenn-Python
Python code for the RPi sensors.

See our [Documentation Website](https://liogl.github.io/BlockPenn-Python).

## Installation
1. Complete deploying the docker image of blockpenn on the RPi. 
2. Follow the steps to set up for `sensor_start_w_sps`
3. Set up crontab to auto start the script in reboot

### sensor_start_w_sps
This is the Python code with all sensors (Air quality, CO2, Humidity & Temp) and OLED display.
There are two ways to set up the environment: 
1. Using a script (recommended)
2. Manually

#### Setting up the environment (Script)
```sh
sudo sh setup_pkg.sh
sh setup_env.sh
```

#### Setting up the environment (Manual)
This is only needed if you didn't run the script to set up the environment.
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
sudo pip3 install Adafruit_SSD1306
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
- Good diagram of particles types (p. 13): https://cdn-learn.adafruit.com/downloads/pdf/pm25-air-quality-sensor.pdf

## Documentation Website
Our [awesome documentation website](https://liogl.github.io/BlockPenn-Python) was created using [docsify](https://docsify.js.org/#/)
