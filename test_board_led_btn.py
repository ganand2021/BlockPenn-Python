#!/usr/bin/env python3
"""
Simple app to test the blockpenn v1 board leds and button
"""

import time
import lgpio as sbc
import sys
import argparse
import datetime
import signal
import atexit

LED1_PIN = 22
LED2_PIN = 23

DHTAUTO = 0
DHT11 = 1
DHTXX = 2

DHT_GOOD = 0
DHT_BAD_CHECKSUM = 1
DHT_BAD_DATA = 2
DHT_TIMEOUT = 3

OUT=20

"""
Has to run after 'sensor' because we run gpiochip_open and closing it in 'sensor'
"""
class led:
    def __init__(self, chip, led_pin, callback=None):
        sbc.gpio_claim_output(chip, led_pin)
        sbc.gpio_write(chip, led_pin, 1)
        self.chip = chip
        self.led_pin = led_pin

    def set_led(self, state):
        sbc.gpio_write(self.chip, self.led_pin, state)


def handle_exit(*err_msg):
#        sbc.gpiochip_close(chip)
#        chip = sbc.gpiochip_open(args.gpiochip)
#        led1.set_led(0)
    sbc.gpiochip_close(chip)
    if err_msg: 
        print("Terminated: code("+str(err_msg[0])+")")
        print("Error message:", err_msg[1])
        exit(err_msg)
    else:
        print("DHT terminated. GPIO closed.")
        exit(0)

chip = sbc.gpiochip_open(0)
# Instantiate a class for each GPIO

# Set the led
atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

S = []

S.append(led(chip, LED1_PIN, 0))  
S.append(led(chip, LED2_PIN, 0))  

led_state = 1
test_cnt = 0

while test_cnt<2:
    try:
        for s in S:
            d = s.set_led(led_state)
            print("Changed led to ",led_state)
        time.sleep(10)
        led_state = 0 if (led_state) else 1
        test_cnt = test_cnt + 1
    except KeyboardInterrupt:
        break

for s in S:
    s.cancel()

sbc.gpiochip_close(chip)