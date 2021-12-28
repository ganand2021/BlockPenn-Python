#!/bin/bash
echo "Setting up RPi Python scripts environment for the first time"
`sudo apt install python3.9-venv`
`python3 -m venv .`
`sudo apt install python3-pip`
`sudo pip3 install influxdb`
`sudo apt install python3-lgpio`
`sudo apt-get install libgpiod2`
