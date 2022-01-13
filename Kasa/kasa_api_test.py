#!/usr/bin/python
import requests, secrets

api_url = "https://wap.tplinkcloud.com"

username = "wm@limerigg.com"
password = "snippet4trick6puttee6detect"

def create_random_uuid():
    uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    uuid = list(uuid)

    uuid_sec = secrets.token_hex(36)

    for uuid_index,uuid_char in enumerate(uuid):
        r = uuid_sec[uuid_index]
        d = int(r,16) & 0x3 | 0x8
    #    (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16)
        if (uuid_char == "x"):
            uuid[uuid_index] = r
        elif (uuid_char == "y"):
            uuid[uuid_index] = format(d,'01x')

    uuid = "".join(uuid)
    return uuid

def get_auth_token(uuid, username, password):
    auth_obj = {
        "method": "login", 
        "params": {
            "appType": "Kasa_Android",
            "cloudUserName": username,
            "cloudPassword": password,
            "terminalUUID": uuid,
        }
    }

    response = requests.post(api_url+"/", json=auth_obj)
#    if (response.status_code == 200): print("Auth success!")
    kasa_token = response.json()["result"]["token"]
    return response.status_code, kasa_token

def get_dev_list(token):
    dev_obj = {"method": "getDeviceList"}
    response = requests.post(api_url+"?token="+token, json=dev_obj)
    return response.status_code, response.json()["error_code"], response.json()["result"]["deviceList"]

def set_dev_state(token, sel_device_id, sel_device_state):
    set_obj = {
        "method": "passthrough", "params": {
            "deviceId": sel_device_id,
            "requestData": "{\"system\":{\"set_relay_state\":{\"state\":" + str(sel_device_state) + "}}}"
        }
    }
    response = requests.post(api_url+"?token="+token, json=set_obj)
    return response.status_code, response.json()["error_code"]

# Authenticate and get token
uuid = create_random_uuid()
print("uuid:",uuid)
[response_code, kasa_token] = get_auth_token(uuid, username, password)
if (response_code == 200): print("Auth success!")
print("kasa_token", kasa_token)
# kasa_token = set the token here if you already have one
# Get device list
[response_code, err_code, dev_list] = get_dev_list(kasa_token)
if (response_code == 200): print("List success!")
if (err_code == 0): print("List has no errors")
print("Identified # of devices:",len(dev_list))

# Select device and turn it off
sel_device = dev_list[0]
print("sel_device", sel_device["deviceId"])
sel_device_id = sel_device["deviceId"]
sel_device_state = 0
[response_code, err_code] = set_dev_state(kasa_token, sel_device_id, sel_device_state)
if (response_code == 200): print("Set success!")
if (err_code == 0): print("Set has no errors")
