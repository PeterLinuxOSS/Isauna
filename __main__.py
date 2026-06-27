

import os
import random
import socket
import traceback
import numpy as np  # noqa: F401
from multiprocessing import Process,Queue,set_start_method,Manager
from multiprocessing.managers import DictProxy,ValueProxy
import time

import json
from paho.mqtt.client import Client, CallbackAPIVersion,MQTTMessage

from log import logger
from variables import *
from templates import *


import requests
import sys



old_data = {}
def client_conn(client_id:str = "testmqtt") -> Client:
    client = Client(callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id)
    client.username_pw_set("mqtt-user", "mqtt9078")
    client.connect("10.10.111.3", 1883)
    return client





def receive_data(data: DictProxy, sock, client: Client):
    global old_data
    if not isinstance(data,DictProxy):
        raise ValueError( f"data object is not a DictProxy its {type(data)}")
    sock.settimeout(5)  # Adjust timeout as needed
    received_data = bytearray()

    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            received_data.extend(chunk)
    except socket.timeout:
        logger.error("Socket timeout occurred. No data received within the specified time.")
        return  # Exit the function early on timeout

    if received_data:
        try:
            lines = received_data.decode("utf-8").splitlines()
            if lines[0] == "HTTP/1.1 200 OK":
                result = remove_chars(lines[-1], chars_to_remove)  # Optimize this function if possible
                logger.info(f"Received binary data: {result}")

                _result = decode_setting(data, result)  # Optimize this function if possible
                if _result:
                    for key, value in _result.items():  # Use iterative update for potential speedup
                        if data.get(key) != value:
                            data[key] = value

                    logger.info(data)
                    
                    old_data_str = json.dumps(old_data)
                    new_data_str = json.dumps(dict(data))

                    if old_data_str != new_data_str:
                        old_data = data.copy()
                        print("updated on mqtt")
                        client.publish("isauna/data", payload=new_data_str, retain=True)  # Publish the string directly
        except Exception as e:
            logger.error(f"Error processing data: {e}")
    else:
        logger.error("error with request")



def process2(data:DictProxy,refresh:ValueProxy):
    client = client_conn("isauna_tx")
    client.on_connect = on_connect_tx
    client.loop_start()
    print("runingig")
    
    try:
    
        while True:
            
            
            logger.debug(data)
            
            
            logger.info(f"Sending message...")
            
            _data = send_message(data,client)
            if _data is None:
                timer =5
            else:
                data.update(_data)
                if data["mode"] == "off":
                    logger.info("sleep")
                    timer = 30
                else:
                    timer = 10 
            for _ in range(0,int(timer)):
                time.sleep(0.5)
                if refresh.value == True:
                    logger.warning("breaking wait loop")
                    refresh.set(False)
                    break
    except Exception:
        logger.error(traceback.format_exc())
        print("---------------------------------------------------")
        logger.exception(traceback.format_exc())
        os._exit(1)
                 
def send_message(data,client):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(message)
    except Exception as ex:
        logger.warning(f"exeption occured")
        logger.error(ex)
        
        return None
    
    else:
        logger.info("else")
        receive_data(data,s,client)
        s.close()
        return data
    
def on_message(client:Client, userdata, msg:MQTTMessage):
    global manager
    
    """if msg.topic == "isauna/data":
        manager.update(json.loads(msg.payload))"""
        
        
    
    if msg.topic == 'homeassistant/switch/isauna/light/set':
        state = bool(int(msg.payload))
        manager["light"] = state
        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
        try:
            requests.get(url="http://10.10.111.2/?Pswrd=bioszauna&Gomb=Light")
        except:
            pass
    elif msg.topic == "homeassistant/switch/isauna/mood_light/set":
        state = bool(int(msg.payload))
        manager["mood_light"] = state
        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
        try:
            requests.get(url="http://10.10.111.2/?Pswrd=bioszauna&Gomb=Mood+Light")
        except:
            pass
    elif msg.topic == "homeassistant/switch/isauna/starry_sky/set":
        state = bool(int(msg.payload))
        manager["starry_sky"] = state
        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
        try:
            requests.get(url="http://10.10.111.2/?Pswrd=bioszauna&Gomb=Starry+Sky")
        except:
            pass    
    elif msg.topic == "homeassistant/switch/isauna/fan/set":
        state = bool(int(msg.payload))
        manager["fan"] = state
        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
        try:
            requests.get(url="http://10.10.111.2/?Pswrd=bioszauna&Gomb=Ventilator")
        except:
            pass        
    elif msg.topic == "homeassistant/number/isauna/set_infra1/set":
        
        state = int(msg.payload)
        manager["set_infra1"] = state
        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
    elif msg.topic == "homeassistant/number/isauna/set_infra2/set":
        
        state = int(msg.payload)
        manager["set_infra2"] = state

        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
    elif msg.topic == "homeassistant/number/isauna/set_temperature/set":
        

        manager["set_temperature"] = int(msg.payload)
     
        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
        
    elif msg.topic == "homeassistant/button/isauna/update_button/set":
       
        value = encode_setting(manager)
        _timeout = 3
        while _timeout >= 0:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    
                    s.connect((HOST, PORT))
                    s.sendall(value.encode())
                    #receive_data(manager,s)
                    refresh.set(True)
            except:
                print("error")
                _timeout-=1
                time.sleep(2)
                continue
            else:
                print("keep going")
                break
            
    elif msg.topic == "homeassistant/select/isauna/set_mode/set":
        manager["set_mode"] = msg.payload.decode()
        
        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
        
    elif msg.topic == "homeassistant/number/isauna/set_min/set":
        manager["set_min"] = int(msg.payload)
        client.publish("isauna/data",payload=json.dumps(dict(manager)),retain=True)
        
def on_connect_tx(client:Client, userdata, flags, rc, *args):    
    print("Connected to {0} with result code {1}, RX".format(userdata, rc))

def on_connect_rx(client:Client, userdata, flags, rc, *args):
    print("Connected to {0} with result code {1}, TX".format(HOST, rc))
    # Subscribe to the hotword detected topic
    client.subscribe("homeassistant/switch/isauna/light/set")
    client.subscribe("homeassistant/switch/isauna/fan/set")
    client.subscribe("homeassistant/light/isauna/starry_sky/set")
    client.subscribe("homeassistant/light/isauna/mood_light/set")
    
    client.subscribe("homeassistant/number/isauna/set_infra1/set")
    client.subscribe("homeassistant/number/isauna/set_infra2/set")
    client.subscribe("homeassistant/button/isauna/update_button/set")
    client.subscribe("homeassistant/select/isauna/set_mode/set")
    client.subscribe("homeassistant/number/isauna/set_temperature/set")
    client.subscribe("homeassistant/number/isauna/set_min/set")
    #client.subscribe("isauna/data")
    
def on_disconnect(client:Client, userdata, flags, rc, *args):
    print(f"Dissconected {rc}")
   
def publish_all(client:Client):
    client.publish("homeassistant/sensor/isauna/temperature/config",
                   payload=json.dumps(temperature_template), retain=True)
    client.publish("homeassistant/sensor/isauna/humidity/config",
                   payload=json.dumps(humidity_template), retain=True)
    client.publish("homeassistant/sensor/isauna/desired_temperature/config",
                   payload=json.dumps(desired_temperature_template), retain=True)
    client.publish("homeassistant/sensor/isauna/mode/config",
                   payload=json.dumps(mode_template), retain=True)
    client.publish("homeassistant/sensor/isauna/infra1/config",
                   payload=json.dumps(infra1_template), retain=True)
    client.publish("homeassistant/sensor/isauna/infra2/config",
                   payload=json.dumps(infra2_template), retain=True)
    client.publish("homeassistant/sensor/isauna/timer/config",
                   payload=json.dumps(timer_template), retain=True)
    client.publish("homeassistant/sensor/isauna/airtimer/config",
                   payload=json.dumps(airtimer_template), retain=True)
    client.publish("homeassistant/switch/isauna/light/config",
                   payload=json.dumps(light_template), retain=True)
    client.publish("homeassistant/switch/isauna/mood_light/config",
                   payload=json.dumps(mood_light_template), retain=True)
    client.publish("homeassistant/switch/isauna/starry_sky/config",
                   payload=json.dumps(starry_sky_template), retain=True)
    client.publish("homeassistant/switch/isauna/air/config",
                   payload=json.dumps(air_template), retain=True)
    
    client.publish("homeassistant/number/isauna/set_temperature/config",
                   payload=json.dumps(set_temperature_template), retain=True)
    client.publish("homeassistant/number/isauna/set_infra1/config",
                   payload=json.dumps(set_infra1_template), retain=True)
    client.publish("homeassistant/number/isauna/set_infra2/config",
                   payload=json.dumps(set_infra2_template), retain=True)
    client.publish("homeassistant/button/isauna/update_button/config",
                   payload=json.dumps(update_button_template), retain=True)
    client.publish("homeassistant/select/isauna/set_mode/config",
                   payload=json.dumps(set_mode_template), retain=True)
    client.publish("homeassistant/number/isauna/set_min/config",
                   payload=json.dumps(set_min_template), retain=True)
    client.publish("isauna/bridge/state", 'online', retain=True)
if __name__ == "__main__":
    mg = Manager()
    manager = mg.dict()
    refresh = mg.Value("refresh",False)
    manager.update(data_tempalte)
    
    client = client_conn("isauna_rx")
    client.on_message = on_message
    client.on_connect = on_connect_rx
    client.on_disconnect  = on_disconnect
    client.will_set("isauna/bridge/state", 'offline', retain=True) 
    publish_all(client)
    _manager = send_message(manager,client)
    if _manager is not None:
        manager.update(_manager)
        manager["set_mode"] = manager["mode"]
        manager["set_temperature"] = manager["desired_temperature"]
        manager["set_infra1"] = manager["infra1"]
        manager["set_infra2"] = manager["infra2"]
        manager["set_min"] = manager["timer"]
    
    client.publish("isauna/data",payload=json.dumps((dict(manager))),retain=True)
    
    p = Process(target=process2, args=(manager,refresh))
    p.start()
    client.loop_forever()
        
    
    
    
    
