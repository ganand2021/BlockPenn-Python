import smbus2

# Define the I2C address of the SPS30 sensor
SPS30_I2C_ADDR = 0x69

# Create an SMBus object for interacting with the I2C bus
bus = smbus2.SMBus(1)  # Use 1 for the Raspberry Pi 2 and 3, use 0 for the Raspberry Pi 1

# Send a command to the SPS30 to start measurements
bus.write_i2c_block_data(SPS30_I2C_ADDR, 0x00, [0x10, 0x00])

# Read the measurement data from the SPS30
data = bus.read_i2c_block_data(SPS30_I2C_ADDR, 0x00, 60)

# Convert the raw data into a list of floating-point values
measurements = [float(x) for x in data]

# Print the measurement values
print("SPS30 measurement values: ", measurements)
