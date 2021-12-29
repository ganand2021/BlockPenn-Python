#!/usr/bin/python
import math, struct, array, time, io, fcntl
import board
import adafruit_shtc3
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Panels
PANEL_NUM = 2
PANEL_DELAY = 10 # In seconds

# T6713 start
bus = 1
addressT6713 = 0x15
I2C_SLAVE=0x0703

class i2c_6713(object):
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
		self.dev = i2c_6713(addressT6713, bus)

	def status(self):
		buffer = array.array('B', [0x04, 0x13, 0x8a, 0x00, 0x01])
		self.dev.write(buffer)
		time.sleep(0.1)
		data = self.dev.read(4)
		buffer = array.array('B', data)
		return buffer[2]*256+buffer[3]

	def gasPPM(self):
		buffer = array.array('B', [0x04, 0x13, 0x8b, 0x00, 0x01])
		self.dev.write(buffer)
		time.sleep(0.1)
		data = self.dev.read(4)
		buffer = array.array('B', data)
		return int((((buffer[2] & 0x3F) << 8) | buffer[3]))
        #return buffer[2]*256+buffer[3]

	def checkABC(self):
		buffer = array.array('B', [0x04, 0x03, 0xee, 0x00, 0x01])
		self.dev.write(buffer)
		time.sleep(0.1)
		data = self.dev.read(4)
		buffer = array.array('B', data)
		return buffer[2]*256+buffer[3]

	def calibrate(self):
		buffer = array.array('B', [0x05, 0x03, 0xec, 0xff, 0x00])
		self.dev.write(buffer)
		time.sleep(0.1)
		data = self.dev.read(5)
		buffer = array.array('B', data)
		return buffer[3]*256+buffer[3]

# T6713 end

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Connect SHTC3
i2c = board.I2C()  # uses board.SCL and board.SDA
sht = adafruit_shtc3.SHTC3(i2c)

# Connect T6713
obj = T6713()

# Configure the display panel
def showPanel(panel_id):
    draw.text((x, top    ), "- "+str(panel_id)+" -", font=font, fill=255)
    if (panel_id == 0):
        draw.text((x, top+8*1), "SYSTEM STATS",  font=font, fill=255)
        draw.text((x, top+8*2), "IP: " + str(IP.decode('utf-8')),  font=font, fill=255)
        draw.text((x, top+8*3), str(CPU.decode('utf-8')), font=font, fill=255)
        draw.text((x, top+8*4), str(MemUsage.decode('utf-8')),  font=font, fill=255)
        draw.text((x, top+8*5), str(Disk.decode('utf-8')),  font=font, fill=255)
    if (panel_id == 1):
        draw.text((x, top+8*1), "SENSORS",  font=font, fill=255)
        draw.text((x, top+8*2), "SHTC3",  font=font, fill=255)
        draw.text((x, top+8*3), str("Temperature: %0.1f C" % temperature),  font=font, fill=255)
        draw.text((x, top+8*4), str("Humidity: %0.1f %%" % relative_humidity),  font=font, fill=255)
        draw.text((x, top+8*5), "T6713 (Status:"+str(bin(obj.status())+")"),  font=font, fill=255)
        draw.text((x, top+8*6), str("PPM: "+str(obj.gasPPM())),  font=font, fill=255)
        draw.text((x, top+8*7), str("ABC State: "+str(obj.checkABC())),  font=font, fill=255)

cur_panel = 1
panel_start = time.time()

while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Get measurements
    temperature, relative_humidity = sht.measurements
    if (time.time()-panel_start > PANEL_DELAY):
        cur_panel = (cur_panel+1) % PANEL_NUM
        panel_start = time.time()
    showPanel(cur_panel)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
