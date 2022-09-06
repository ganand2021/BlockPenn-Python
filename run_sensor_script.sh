#!/bin/bash
# Wait for influxdb to start
echo "Sensor script started"
until pids=$(pidof influxd)
do   
    sleep 5
done
echo "Influx is running, starting sensors python script"
cd /home/ubuntu/blockpenn-python         
while true
do
    sudo python3 sensor_start_w_sps_v2.py
    sleep 5
    echo "Restarting code..."
done
