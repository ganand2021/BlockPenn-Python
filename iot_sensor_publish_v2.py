# Standard library imports
import datetime
import json
import logging
import logging.handlers
import os
import sys
import time
from dotenv import load_dotenv
import random

# Third-party library imports
from PIL import Image, ImageDraw, ImageFont
import adafruit_shtc3
import board
import RPi.GPIO as GPIO
from awscrt import mqtt
from awsiot import mqtt_connection_builder

# Local module imports
from AWSHandler.functions import (
    on_connection_interrupted, on_connection_resumed, on_message_received,
    on_connection_success, on_connection_failure, on_connection_closed
)
from config import *
from device_info import get_device_data
from Kasa import KasaDevices
from SPS30.i2c import SPS30_I2C
from T6713 import t6713
import Adafruit_SSD1306

# Load environment variables and set constants
load_dotenv("../Certificates/Kasa.env")
os.environ['OPENSSL_CONF'] = OPENSSL_CONF


# Configure logging
log_fname = os.path.join(LOG_DIR, os.path.splitext(os.path.basename(__file__))[0]+".log")
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)
log_handler = logging.handlers.RotatingFileHandler(
	log_fname,
	maxBytes=LOG_MAX_BYTES, 
	backupCount=LOG_BACKUP_COUNT
 )
logger.addHandler(log_handler)
logging.basicConfig(
	handlers=[log_handler],
	format='%(asctime)s [%(levelname)-8s] %(message)s',
	level=logging.DEBUG,
	datefmt='%Y-%m-%d %H:%M:%S')
logger.debug('Script started')

#GPIO Setup
GPIO.setwarnings(False) # Ignore warning (TBD)
GPIO.setmode(GPIO.BCM) # Use BCM instead of physical mapping
# GPIO classes Definition: led & btn
class led:
	global GPIO
	def __init__(self, led_pin, callback=None):
		GPIO.setup(led_pin, GPIO.OUT)
		self.led_pin = led_pin

	def set_led(self, state):
		GPIO.output(self.led_pin, state)

class btn:
	global GPIO
	def __init__(self, btn_pin, callback=None):
		GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
		GPIO.add_event_detect(btn_pin,GPIO.FALLING,callback=callback) 
		self.btn_pin = btn_pin


def button_callback(channel):
	global cur_panel
	logging.info("Button was pushed! (GPIO "+str(channel)+")")
	if (channel == LBTN_PIN) : 
		if (cur_panel > 0): cur_panel = (cur_panel-1) % PANEL_NUM
		else : cur_panel = PANEL_NUM - 1
	if channel == RBTN_PIN: cur_panel = (cur_panel+1) % PANEL_NUM

logging.info('LED and BTN Setup: Started')
red_led = led(LED1_PIN, 0)
green_led = led(LED2_PIN, 0)
l_btn = btn(LBTN_PIN, callback=button_callback)
r_btn = btn(RBTN_PIN, callback=button_callback)
logging.info('LED and BTN Setup: Completed Successfully')
green_led.set_led(1)
red_led.set_led(1)
time.sleep(1)
red_led.set_led(0)

##OLED Setup
# Panels
cur_panel = 1
# Raspberry Pi pin configuration:
logging.debug('OLED Setup: Started')
RST = None     # on the PiOLED this pin isnt used
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
try:
	disp.begin()
except Exception as e:
	logging.exception("Main crashed during OLED setup. Error: %s", e)
	  
# Clear display.
disp.clear()
disp.display()

def showPanel(panel_id):
	try:
		data = getData()
		draw.text((x, top    ), "- "+str(panel_id)+" -", font=font, fill=255)
		if (panel_id == 0):
			draw.text((x, top+8*1), "SYSTEM STATS",  font=font, fill=255)
			draw.text((x, top+8*2), "IP: " + str(data["IP Address"]),  font=font, fill=255)
			draw.text((x, top+8*3), str(data["CPU Load"]), font=font, fill=255)
			draw.text((x, top+8*4), str(data["Memory Usage"]),  font=font, fill=255)
			draw.text((x, top+8*5), str(data["Disk Usage"]),  font=font, fill=255)
		if (panel_id == 1):
			draw.text((x, top+8*1), "SENSORS: Tmp, Hum, CO2",  font=font, fill=255)
			draw.text((x, top+8*2), "SHTC3",  font=font, fill=255)
			draw.text((x, top+8*3), str("Temperature: %0.1f C" % data["Temperature"]),  font=font, fill=255)
			draw.text((x, top+8*4), str("Humidity: %0.1f %%" % data["Humidity"]),  font=font, fill=255)
## T6713
			draw.text((x, top+8*5), "T6713 (Status:"+str(data["CO2 Sensor Status"])+")",  font=font, fill=255)
			draw.text((x, top+8*6), str("PPM: "+str(data["CO2 Concentration"])),  font=font, fill=255)
			draw.text((x, top+8*7), str("ABC State: "+str(data["CO2 ABC State"])),  font=font, fill=255)
## T6713
		if (panel_id == 2):
			draw.text((x, top+8*1), "SENSORS: Air Quality",  font=font, fill=255)
## SPS30	
			draw.text((x, top+8*2), str("PM1.0: %0.1f µg/m3" % data["pm10 standard"]),  font=font, fill=255)
			draw.text((x, top+8*3), str("PM2.5: %0.1f µg/m3" % data["pm25 standard"]),  font=font, fill=255)
			draw.text((x, top+8*4), str("PM10 : %0.1f µg/m3" % data["pm100 standard"]),  font=font, fill=255)
			draw.text((x, top+8*5), str("NC1.0: %0.1f 1/cm3" % data["particles 10um"]),  font=font, fill=255)
			draw.text((x, top+8*6), str("NC4.0: %0.1f 1/cm3" % data["particles 40um"]),  font=font, fill=255)
			draw.text((x, top+8*7), str("Typical Particle Size: %0.1f µm" % data["tps"]),  font=font, fill=255)
## SPS30
	except Exception as e:
		green_led.set_led(0)
		# GPIO.cleanup()
		logging.exception("main crashed during panel display. Error: %s", e)

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (disp.width, disp.height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
# Draw a black filled box to clear the image.
draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = disp.height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
# Load default font.
font = ImageFont.load_default()
logging.debug('OLED Setup: Completed Successfully')

##SHTC3 Setup
# Connect SHTC3
logging.debug('SHTC3 Setup: Started')
i2c = board.I2C()  # uses board.SCL and board.SDA
sht = adafruit_shtc3.SHTC3(i2c)
logging.debug('SHTC3 Setup: Completed Successfully')

##T6713 Setup
logging.debug('T6713 Setup: Started')
obj_6713 = t6713.T6713()
logging.debug('T6713 Setup: Completed Successfully')

##SPS30 Setup
logging.debug('SPS30 Setup: Started')
sps = SPS30_I2C(i2c)
logging.debug('SPS30 Setup: Completed Successfully')

##Kasa Setup
logging.debug('Kasa Setup: Started')
kasa_username = os.environ.get("USERNAME")
kasa_password = os.environ.get("PASSWORD")
kasaObject = KasaDevices.SmartPlugs()
uuid = kasaObject.create_random_uuid()
response_code = kasaObject.set_auth_token(uuid, kasa_username, kasa_password)
[response_code, err_code, dev_list, n_kasa_devices] = kasaObject.get_set_dev_list()
response_code = kasaObject.handle_devices()
logging.debug('Kasa Setup: Completed Successfully')

##AWS Setup
logging.debug('AWS Setup: Started')
# Create the proxy options if the data is present in cmdData
proxy_options = None

##Certificates Directory - Find Keys
# auth_paths[0] : Thing Certificate
# auth_paths[1] : Private Key
# auth_paths[2] : CA1 General Certificate 
# auth_paths[3] : Thing Identifier
certificates_path = "../Certificates"
auth_paths = [None]*4
for file_path in os.listdir(certificates_path):
    if file_path.endswith("-certificate.pem.crt"):
        auth_paths[0] = os.path.join(certificates_path, file_path)
    elif file_path.endswith("-private.pem.key"):
        auth_paths[1] = os.path.join(certificates_path, file_path)
        auth_paths[3] = file_path.split("-")[0]
    elif file_path.endswith("CA1.pem"):
        auth_paths[2] = os.path.join(certificates_path, file_path)

# Create a MQTT connection from the command line data
mqtt_connection = mqtt_connection_builder.mtls_from_path(
	endpoint=MQTT_ENDPOINT,
	cert_filepath = auth_paths[0],
	pri_key_filepath = auth_paths[1],
	ca_filepath = auth_paths[2],
	on_connection_interrupted=on_connection_interrupted,
	on_connection_resumed=on_connection_resumed,
	client_id=auth_paths[3],
	clean_session=False,
	keep_alive_secs=MQTT_KEEP_ALIVE_SECS,
	http_proxy_options=proxy_options,
	on_connection_success=on_connection_success,
	on_connection_failure=on_connection_failure,
	on_connection_closed=on_connection_closed)

connect_future = mqtt_connection.connect()
# Future.result() waits until a result is available
connect_future.result()
print("Connected!")
logging.debug('AWS Setup: Completed Successfully')

def getData():
	device_data = get_device_data()
	temperature, relative_humidity = sht.measurements
	data = {
		"Timestamp": datetime.datetime.now().timestamp(),
		"RPI Identifier": auth_paths[3],
        "Temperature" : float(temperature),
        "Humidity" : float(relative_humidity),
        "CO2 Sensor Status" : str(obj_6713.status()),
        "CO2 Concentration" : float(obj_6713.gasPPM()),
        "CO2 ABC State" : float(obj_6713.checkABC())
    }
	if n_kasa_devices != 0:
		kasa_data = kasaObject.get_power_energy_data()
		{data.update(plug_data) for _, plug_data in kasa_data.items()}
	data.update(sps.read())
	data.update(device_data)
	return data
        
if __name__ == "__main__":
    try:
        green_led_status = 1
        db_sample_start = time.time()
        oled_panel_start = time.time()
        logger.debug(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(oled_panel_start))}: main started")
        draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)

        while True:
            green_led_status ^= 1
            logger.debug(f'green_led_status: {green_led_status}')
            green_led.set_led(green_led_status)
            draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)
            if time.time() - oled_panel_start > PANEL_DELAY:
                cur_panel = (cur_panel + 1) % PANEL_NUM
                oled_panel_start = time.time()
            showPanel(cur_panel)

            if time.time() - db_sample_start > DB_SAMPLE_PERIOD:
                logger.debug('Writing samples to the DB')
                mqtt_connection.publish(
					topic="data/measurement",
					payload=json.dumps(getData()),
					qos=mqtt.QoS.AT_LEAST_ONCE
     			)
                logger.debug('Samples Written to DB Successfully')
                db_sample_start = time.time()

            disp.image(image)
            disp.display()
            time.sleep(1)

    except Exception as e:
        logger.exception("Unhandled exception occurred: %s", e)
        # Disconnect
        logger.info("Disconnecting...")
        disconnect_future = mqtt_connection.disconnect()
        disconnect_future.result()
        logger.info("Disconnected!")
