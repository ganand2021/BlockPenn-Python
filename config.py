# GPIO configuration
LED1_PIN = 23 # red 
LED2_PIN = 22 # green
LBTN_PIN = 27 # pull-down - Not working. Design connects it ground the RPI GPIO.
MBTN_PIN = 17 # pull-down
RBTN_PIN = 4  # pull-down

# Sample periods
DB_SAMPLE_PERIOD = 10 # Write the samples to the DB every DB_SAMPLE_PERIOD seconds
PANEL_DELAY = 30

# Logging configuration
LOG_DIR = "../Logs"
LOG_MAX_BYTES = 10*1024*1024 #10MB
LOG_BACKUP_COUNT = 5

# MQTT configuration
MQTT_ENDPOINT = "a3cp1px06xaavc-ats.iot.us-east-1.amazonaws.com"
MQTT_KEEP_ALIVE_SECS = 30

# SSL configuration
OPENSSL_CONF = "./openssl.conf"

# OLED configuration
PANEL_NUM = 3