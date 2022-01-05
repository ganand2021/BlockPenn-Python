#!/usr/bin/python
import math, struct, array, time, io, fcntl
import subprocess

# Panels
PANEL_NUM = 2
PANEL_DELAY = 10 # In seconds

# T6713 
bus = 1
addressT6713 = 0x15
I2C_SLAVE=0x0703

class i2c_obj(object):
	def __init__(self, device, bus):
		self.fr = io.open("/dev/i2c-"+str(bus), "rb", buffering=0)
		self.fw = io.open("/dev/i2c-"+str(bus), "wb", buffering=0)
		# set device address
		fcntl.ioctl(self.fr, I2C_SLAVE, device)
		fcntl.ioctl(self.fw, I2C_SLAVE, device)
	def write(self, bytes):
		self.fw.write(bytes)
	def read(self, bytes):
		return self.fr.read(bytes)
	def close(self):
		self.fw.close()
		self.fr.close()

class T6713(object):
	def __init__(self):
		self.dev = i2c_obj(addressT6713, bus)

	def status(self):
		buffer = array.array('B', [0x04, 0x13, 0x8a, 0x00, 0x01])
		self.dev.write(buffer)
		time.sleep(0.01)
		data = self.dev.read(4)
		buffer = array.array('B', data)
		return buffer[2]*256+buffer[3]

	def send_cmd(self, cmd):
		buffer = array.array('B', cmd)
		self.dev.write(buffer)
		time.sleep(0.01)
		data = self.dev.read(5)
		buffer = array.array('B', data)
		return buffer

	def reset(self):
		buffer = array.array('B', [0x04, 0x03, 0xe8, 0x00, 0x01])
		self.dev.write(buffer)
		time.sleep(0.01)
		data = self.dev.read(5)
		buffer = array.array('B', data)
		cmd_result = 1
		if ((buffer[2] == 0xe8) & (buffer[3] == 0xff) & (buffer[4] == 0x00)): cmd_result = 0 
		return buffer

	def gasPPM(self):
		buffer = array.array('B', [0x04, 0x13, 0x8b, 0x00, 0x01])
		self.dev.write(buffer)
		time.sleep(0.01)
		data = self.dev.read(4)
		buffer = array.array('B', data)
		return int((((buffer[2] & 0x3F) << 8) | buffer[3]))
        #return buffer[2]*256+buffer[3]

	def checkABC(self):
		buffer = array.array('B', [0x04, 0x03, 0xee, 0x00, 0x01])
		self.dev.write(buffer)
		time.sleep(0.01)
		data = self.dev.read(4)
		buffer = array.array('B', data)
		return buffer[2]*256+buffer[3]

	def calibrate(self):
		buffer = array.array('B', [0x05, 0x03, 0xec, 0xff, 0x00])
		self.dev.write(buffer)
		time.sleep(0.01)
		data = self.dev.read(5)
		buffer = array.array('B', data)
		return buffer[3]*256+buffer[3]

# SHTC3

addressSHTC3 = 0x70

class SHTC3(object):
	def __init__(self):
		self.dev = i2c_obj(addressSHTC3, bus)

	def soft_reset(self):
		buffer = array.array('B', [0x80, 0x5d])
		self.dev.write(buffer)
		time.sleep(0.1)

	def read_measurement(self):
		buffer = array.array('B', [0x35, 0x17])
		self.dev.write(buffer)
		time.sleep(0.1)
		buffer = array.array('B', [0x78, 0x66])
		self.dev.write(buffer)
		time.sleep(0.1)
		a = self.dev.read(6)
		time.sleep(0.1)
		buffer = array.array('B', [0xb0, 0x98])
		self.dev.write(buffer)
		time.sleep(0.1)
		temp = 175*((a[0]*256+a[1])/2**16)-45
		humd = 100*((a[3]*256+a[4])/2**16)
		return temp, humd

obj = T6713()
t6713_reset = obj.reset()
print("T6713 reset returned:")
print(','.join(format(x, '02x') for x in t6713_reset))

shtc3 = SHTC3()

while True:
    [shtc3_t, shtc3_h] = shtc3.read_measurement()
    print("t,h", shtc3_t, shtc3_h)
    time.sleep(1)

