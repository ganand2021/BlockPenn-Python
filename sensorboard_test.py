#!/usr/bin/python
# Aimed to test new boards w/o any sensors and oled
import math, struct, array, time, io, fcntl
import logging, os, inspect, logging.handlers
import board

import subprocess

# for the leds and buttons
import RPi.GPIO as GPIO # Import RPi.GPIO library

LED1_PIN = 22 # red 
LED2_PIN = 23 # green

LBTN_PIN = 4 # pull-down
MBTN_PIN = 17 # pull-down
RBTN_PIN = 27 # pull-down

LED_R = 0
LED_L = 0

# Start logging
log_fname = os.path.splitext(os.path.basename(__file__))[0]+".log"
log_level = logging.DEBUG

logger = logging.getLogger('MyLogger')
logger.setLevel(log_level)

# Adding rotating log
log_handler = logging.handlers.RotatingFileHandler(
	log_fname,
	maxBytes=200000, 
	backupCount=5)
logger.addHandler(log_handler)

logging.basicConfig(
	handlers=[log_handler],
	format='%(asctime)s [%(levelname)-8s] %(message)s',
	level=log_level,
	datefmt='%Y-%m-%d %H:%M:%S')
logger.debug('Script started')

# GPIO classes: led & btn
class led:
	def __init__(self, led_pin, callback=None):
		GPIO.setup(led_pin, GPIO.OUT)
		self.led_pin = led_pin

	def set_led(self, state):
		GPIO.output(self.led_pin, state)

class btn:
	def __init__(self, btn_pin, callback=None):
		GPIO.setup(btn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
		GPIO.add_event_detect(btn_pin,GPIO.FALLING,callback=callback) 
		self.btn_pin = btn_pin

# Start the lgpio
GPIO.setwarnings(False) # Ignore warning (TBD)
GPIO.setmode(GPIO.BCM) # Use BCM instead of physical mapping

def button_callback(channel):
	global cur_panel
	logging.info("Button was pushed! (GPIO "+str(channel)+")")
	if (channel == LBTN_PIN) : 
		LED_L = (1 if LED_L == 0 else 0) 
	if (channel == MBTN_PIN) :
        LED_M = 1 if LED_M == 0 else LED_M = 0 
	if (channel == RBTN_PIN) :
        LED_R = 1 if LED_R == 0 else LED_R = 0 

# Set the leds & btns
logging.info('Setting leds and buttons')
red_led = led(LED1_PIN, 0)
green_led = led(LED2_PIN, 0)
l_btn = btn(LBTN_PIN, callback=button_callback)
m_btn = btn(MBTN_PIN, callback=button_callback)
r_btn = btn(RBTN_PIN, callback=button_callback)
logging.info('Completed setting leds and buttons')
green_led.set_led(1)

red_led.set_led(1)
time.sleep(1)
red_led.set_led(0)

def main():
	green_led_status = 1
	panel_start = time.time()
	str_panel_start = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(panel_start))
	print(str_panel_start+": main started")
	while True:
		# Blink the green led
		logging.debug('green_led_status'+str(green_led_status))
		green_led.set_led(green_led_status)
		green_led_status = 0 if green_led_status else 1 
        red_led.set_led(LED_L or LED_R or LED_M)
		time.sleep(1)

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		green_led.set_led(0)
		# red_led.set_led(1)
		GPIO.cleanup()
		logging.exception("main crashed. Error: %s", e)
