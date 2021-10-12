#!/usr/bin/env python3
"""
Simulated temp and humidity readings for testing purposes.
"""

import time
import logging
import random
# ToDo: add different types of sensor, adjust values per previous one, connect to global to do so, connect to recording function 
# Randomize with velocity

# Velocity is in units/hour
# Will work well if called at least once per hour
class sim_sensor:
    def __init__(self, sensor_type = "temp", initial_val = "23.0", initial_velocity = "1"):
        self.sensor_type = sensor_type
        self.initial_val = initial_val
        self.cur_val = initial_val
        self.velocity = initial_velocity
        self.prev_time = time.time()
        if (sensor_type == "temp"):
            self.sensor_std = 1
        elif (sensor_type == "humidity"):
            self.sensor_std = 4
        else:
            logging.error("get_sim_value: unknown sensor type ("+str(sensor_type)+")")

    def read(self, time_set):
        cur_time = time_set
        time_dif = int(cur_time - self.prev_time)
        self.prev_time = cur_time
        read_val = self.cur_val + self.velocity * time_dif/3600
        self.cur_val = read_val
        self.velocity += random.normalvariate(0+(self.initial_val - read_val), self.sensor_std)*time_dif/600
        # set new values
        return read_val

if __name__ == "__main__":
    import sys
    import argparse
    import sim_test as DHT_SIM
    import datetime
    import signal
    import atexit

    def handle_exit(*err_msg):
        if err_msg: 
            print("Terminated: code("+str(err_msg[0])+")")
            print("Error message:", err_msg[1])
            exit(err_msg)
        else:
            print("DHT terminated. GPIO closed.")
            exit(0)

    atexit.register(handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)

    time_now = time.time()
    time_future = time.time()+60*1200
    temp_sensor = DHT_SIM.sim_sensor("temp", 22.0, 0)
    print("{:s}".format(datetime.datetime.fromtimestamp(time_now).strftime('%Y-%m-%d %H:%M:%S')))
    print("{:s}".format(datetime.datetime.fromtimestamp(time_future).strftime('%Y-%m-%d %H:%M:%S')))
    time_delta = int(time_future-time_now)
    for x in range(0 ,time_delta, 600):
        time_cur = time_now + x
        temperature = temp_sensor.read(time_set = time_cur)
        print("{:s} t={:3.3f}".format(datetime.datetime.fromtimestamp(time_cur).strftime('%Y-%m-%d %H:%M:%S'), temperature))

    # while True:
    #     try:
    #         time.sleep(5)
    #     except KeyboardInterrupt:
    #         print("Keyboard interrup")
    #         break

