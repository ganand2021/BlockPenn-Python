from influxdb import InfluxDBClient
from datetime import datetime
import time

import adafruit_dht
from board import D4

# DB Variables
DB_VAR_IP = '127.0.0.1'
DB_VAR_PORT = 8086
DB_VAR_USER = 'root'
DB_VAR_PASS = 'root'
DB_VAR_DB_NAME = 'db0' #'Meyerson_Deployment'


def createDatabase():
    client = InfluxDBClient(DB_VAR_IP, DB_VAR_PORT, DB_VAR_USER, DB_VAR_PASS, DB_VAR_DB_NAME)
    client.create_database(DB_VAR_DB_NAME)
    return client

dht_device = adafruit_dht.DHT22(D4)
client = createDatabase()

def ganacheLogger(data, Measurement, Unit, MAC_Address, unit_descrip, sensor_name, mfg_name):
    global client
    # This is per data Transmission
    json_body = []
    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    json_body.append(
        {
            "measurement": Measurement,         # CO2, Temp, etc 
            "tags": {
                "ProjectID": "“BlockPenn”",            # CharacterString, project identifier, eg. “BlockPenn”
                "ProjectDeployment": "Deployment 1",        # CharacterString, phase of the project
                "UnitDescription": unit_descrip,        # CharacterString, e.g. "degree Celsius"
                "UnitSymbol": Unit,        # CharacterString, e.g. "°C"
                "MACAddress": MAC_Address,            # CharacterString
                "TimeZone": "Philadelphia",            # CharacterString
                "Address": "1908 Mt Vernon St",                 # CharacterString
                "BuildingID": "N/A",                   # CharacterString
                "BuildingName": "Max's Apartment",               # CharacterString
                "RoomNumber": "3F",       # CharacterString
                "SensorName": sensor_name,               # CharacterString, eg. DHT22
                "SensorManufacturer": mfg_name        # CharacterString, company name
            },
            "LocalTime": current_time,              # TM_Instant (ISO 8601 Time string) '%Y-%m-%dT%H:%M:%SZ' 
            "fields": {
                "value": data           # Any
            }
        }
    )
    client.write_points(json_body)

def main():
    while 1:
        try:
            time.sleep(1)
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            print("Temp: ", temperature, "c Humidity: ", humidity,"%")
            ganacheLogger(float(temperature), "Temperature", "C", "MAC_Address_lior_t", "unit_descrip", "DHT22", "Aosong Electronics Co.")	
            ganacheLogger(float(humidity), "Humidity", "%", "MAC_Address_lior_h", "unit_descrip", "DHT22", "Aosong Electronics Co.")
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error
    print("Ending session and closing connection... Goodbye!")
    

if __name__ == "__main__":
    main() 


