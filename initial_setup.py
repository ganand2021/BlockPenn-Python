import requests
from dotenv import load_dotenv
import os
from bp_env_utils import edit_env_file
from influxdb_utils import create_influxdb_bucket

load_dotenv()

URL_ENDPOINT = os.environ['INFLUX_URL']
ENV_PATH = ".env"

name = str(input("Enter Name: "))
description = str(input("Enter Description: "))
location = str(input("Enter Location: "))

my_obj = {
    "name": name,
    "description": description,
    "location": location
}

auth_creds = requests.post(URL_ENDPOINT+"/auth_creds/", json=my_obj)
auth_creds = auth_creds.json()

edit_env_file(ENV_PATH, "RPI_ID", str(auth_creds['RPI ID']))
edit_env_file(ENV_PATH, "INFLUX_BUCKET", str(auth_creds['Bucket ID']))
edit_env_file(ENV_PATH, "INFLUX_ORG", str(auth_creds['ORG Name']))
edit_env_file(ENV_PATH, "INFLUX_TOKEN", str(auth_creds['TOKEN']))

print("ENV Setup Finished!")

create_influxdb_bucket(
    bucket=auth_creds['Bucket ID'], 
    org_name=auth_creds['ORG Name'], 
    token=auth_creds['TOKEN'], 
    url=os.environ['INFLUX_URL']+ ":8086", 
    rpi_id=auth_creds['RPI ID'])

print("Influx Setup Finished!")
