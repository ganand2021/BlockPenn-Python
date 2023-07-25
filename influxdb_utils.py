import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
from datetime import datetime
import pytz
from bp_env_utils import return_env_variables

def create_influxdb_bucket(bucket, org_name, token, url, rpi_id):  
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org_name
    )
    influxdb_org_api = influxdb_client.OrganizationsApi(client)
    influxdb_buckets_api = client.buckets_api()
    
    orgs = influxdb_org_api.find_organizations()
    for org in orgs:
        if org.name == org_name:
            my_org_id = org.id
    
    new_bucket = influxdb_client.domain.bucket.Bucket(
        name=bucket,
        retention_rules=[],
        org_id=my_org_id
    )
    influxdb_buckets_api.create_bucket(new_bucket)
    

def influx_write(data):
    bucket, org, token, url, rpi_id = return_env_variables()
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)

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