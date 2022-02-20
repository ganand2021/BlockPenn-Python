#!/usr/bin/env python3
"""
Simple app to test the blockpenn v1 board leds and button
"""

import time
import lgpio as sbc
import sys
import argparse
import datetime

LED1_PIN = 22 # green 
LED2_PIN = 23 # red

BTN1_PIN = 4 # Bottom, Hi by default
BTN2_PIN = 27 # Into the center of the PCB, Hi by default

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

class btn:
    def __init__(self, chip, btn_pin, callback=None):
        sbc.gpio_claim_input(chip, btn_pin)
        self.chip = chip
        self.btn_pin = btn_pin

    def sts_btn(self):
        return sbc.gpio_read(self.chip, self.btn_pin)

chip = sbc.gpiochip_open(0)
# Instantiate a class for each GPIO

# Set the led
led1 = led(chip, LED1_PIN, 0)
led2 = led(chip, LED2_PIN, 0)
btn1 = btn(chip, BTN1_PIN)
btn2 = btn(chip, BTN2_PIN)

led_state = 1
test_cnt = 0

while (btn1.sts_btn() or btn2.sts_btn()):
    try:
        led1.set_led(led_state)
        led2.set_led(led_state)
        print("btn1 is ", btn1.sts_btn())
        print("btn2 is ", btn2.sts_btn())
        time.sleep(1)
        led_state = 0 if (led_state) else 1
        test_cnt = test_cnt + 1
    except KeyboardInterrupt:
        break

sbc.gpiochip_close(chip)