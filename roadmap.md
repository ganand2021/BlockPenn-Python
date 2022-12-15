# Development Roadmap

## Done
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
- [x] Add a script for setup
- Functionality:
- [x] Connect controls: button
- [x] Connect controls: leds
- [x] Add functionality to buttons via events
- [x] Add blinking ok led
- [x] Add plug load monitoring
- [x] Add documentation
- [x] Add testing script for the PCB
- [x] Adjust for V2
- [x] V2: Add 3rd button support, switch leds pins

## Future potential features
- Implement requirements.txt: `pip3 install -r requirements.txt`
- To create the requirements.txt: `pip3 freeze > requirements.txt`
- Consider using `sensors` (`sudo apt install lm-sensors`) to check the internal temperature
- Add more graphics to OLED display
- Allow ENV file to control the configuration 
- Remove old scripts / put in a seperate folder