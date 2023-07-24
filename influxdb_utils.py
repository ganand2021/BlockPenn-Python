import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from datetime import datetime
import pytz
import uuid
import os
from dotenv import load_dotenv

def edit_env_file(env_file, variable_name, new_value):
    # Open the .env file in read mode
    with open(env_file, "r") as f:
        lines = f.readlines()

    # Update the value in the lines
    updated_lines = []
    for line in lines:
        line = line.strip()
        if line and "=" in line:
            key, value = line.split("=", 1)
            if key == variable_name:
                line = f"{key}={new_value}"
        updated_lines.append(line)

    # Write the updated lines back to the .env file
    with open(env_file, "w") as f:
        f.write("\n".join(updated_lines))

load_dotenv()

bucket = os.environ['INFLUX_BUCKET'] 
org = os.environ['INFLUX_ORG']
token = os.environ['INFLUX_TOKEN']
url = os.environ['INFLUX_URL']
rpi_id = os.environ['RPI_ID']

if rpi_id == "":
    rpi_id = uuid.uuid1().hex
    print(rpi_id)
    edit_env_file(".env", "RPI_ID", rpi_id)

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# # Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

def influx_write(data):
    global write_api
    tz = pytz.timezone('America/New_York')
    current_time = datetime.utcnow()
    current_time = tz.fromutc(current_time)
    data['time'] = current_time
    data['record_time'] = current_time
    data['id'] = rpi_id
    df = pd.DataFrame(data, index=[0])
    df.set_index('time', inplace=True)
    write_api.write(bucket, org, record=df, data_frame_measurement_name='rpi_test')
    print("Wrote data point:")
    print(df.head())