import socket
import numpy as np
from log import  logger  # noqa: F401
import json
from paho.mqtt.client import Client,CallbackAPIVersion
from multiprocessing.managers import DictProxy

HOST = "10.10.111.2"  # Replace with server IP address if necessary
PORT = 80  # Replace with server port if necessary
message = b"$$$c0000000000000000000000$3ajlpybvmb"
password_enc = "3ajlpybvmb"


chars_to_remove = ['$$$','$$A','$$B','$$C','','','&&&']
data_tempalte = {
        "hwversion":3,
        "mode":"off",
        "set_mode":"off",
        'desired_temperature': 0,
        "set_temperature":30,
        
        'infra1': 0,
        'infra2': 0,
        "set_infra1":0,
        "set_infra2":0,
        'timer': f"0:0:0",
        #"set_timer":"0:0:0",
        "set_min":0,
        
        'light': False,
        'mood_light': False,
        'starry_sky': False,
        'salt_wall': False,
        'air': False,
        'temperaturerror': True,
        'currentsaunatemp': 255,
        'steamerror': True,
        'currentsteam': 255,
        'steam': 0,
        'airtimer': f"0:0:0",
       
        'watererror': True,
        "floorheattemp":0,
        "steam_on":0,
        
        "floortemp":5 #temperaltemp
        }

def remove_chars(text, chars_to_remove):
  for char in chars_to_remove:
    text = text.replace(char, "")
  return text

def client_conn(client_id:str = "testmqtt") -> Client:
    client = Client(callback_api_version=CallbackAPIVersion.VERSION2,
        client_id=client_id)
    client.username_pw_set("mqtt-user", "mqtt9078")
    client.connect("10.10.111.3", 1883)
    return client



def decode_setting(data:DictProxy,result:str):
    """
    Decodes data from a given string and updates a dictionary.

    Args:
        result: The input string containing encoded data.
        data: A dictionary to store the decoded data.
    """
    
    
    hwversion = data.get("hwversion", 0)  # Assuming a default value if not found

    

    if result.startswith("c"):
        print("Ignored")
        return

    # ... Rest of the decoding logic, updated to use dictionary operations

    # Example:
    flags = {"I": "infra", "F": "finn", "G":"steam","0":"off"}
    
    data["mode"] = flags[result[2]]
    data["desired_temperature"] = int(result[5:7], 16)    
    
    

    # Decode infra data
    data["infra1"] = (ord(result[3]) - 48) * 10
    data["infra2"] = (ord(result[4]) - 48) * 10
    

    # Decode operate times
    minutes = int(result[7:9], 16) * 256 + int(result[9:11], 16)
   
    data["timer"] = f"{minutes // 60}:{minutes % 60}:{int(result[11:13], 16)}"
    # Decode lights
    light_dec = ord(result[13]) - 48
    
    data["light"] = True if((light_dec & 0x01) >=1) else False 
    data["mood_light"] = True if((light_dec & 0x02) >=1) else False 
    data["starry_sky"] = True if((light_dec & 0x04) >=1) else False 
    data["salt_wall"] = True if((light_dec & 0x08) >=1) else False 
    data["air"] = True if((light_dec & 0x10)>=1) else False 

    # Decode current cabin temperature
    current_temp = int(result[14:16], 16)
    
    data["temperaturerror"] = True if current_temp == 255 else False
    data["currentsaunatemp"] = current_temp

    # Decode measured steam
    current_steam = int(result[16:18], 16)
    data["steamerror"] = True if current_steam == 255 else False
    data["currentsteam"] = current_steam
    data["steam"] = int(result[20:22], 16)

    # Decode ventilator time
    air_time = ord(result[22]) - 48

    data["airtimer"] = f"{air_time // 60}:{air_time % 60}:{ord(result[18]) - 48}"
    # Decode water error
    data["watererror"] = False
    if data["mode"] == "steam":
        data["watererror"] = result[23]

    # Decode floor heat (only for hwversion > 0)
    if hwversion > 0:
        data["floorheatcurtemp"] = int(result[28:30], 16)
        data["floorheaterror"] = True if data["floorheatcurtemp"] == 255 else False
        floor_temp = int(result[24:26], 16)
        if floor_temp < 40:
            data["floorheaton"] = False
        else:
            if not np.isnan(floor_temp):
                data["floorheatemp"] = floor_temp - 50
                data["floorheaton"] = True
        data["temperaltemp"] = int(result[26:28], 16)
    return data

def pad2(width, string, padding=' '):
  """Pads a string to a minimum width using the specified padding character.

  Args:
      width: The minimum desired length of the padded string.
      string: The string to be padded.
      padding: The character to use for padding (defaults to space).

  Returns:
      The padded string.
  """

  # Ensure string length considers padding character size
  string_len = len(f"{string}")  # Original string length
  total_len = string_len + len(padding) * (width - string_len)  # Consider padding

  # Pad if needed
  if total_len < width:
    padding_count = width - total_len
    padding_string = padding * padding_count
    return padding_string + string
  else:
    return string

def pad(width, string, padding="0"):
    if isinstance(string, int):  # Check if input is a number
        string = str(hex(string))[2:].lower()  # Convert to hex, remove '0x', and uppercase
    elif isinstance(string, str):  # Check if input is a string
        string = "".join([hex(ord(c))[2:].lower() for c in string])
    else:
        raise TypeError("Unsupported input type for string")

    # Padding logic
    return padding * (width - len(string)) + string  # No recursion needed



def encode_setting(data,code_p="", other_data=None):
    code = "$$$AC"
    flags = {"infra": "WI", "finn": "WF", "steam":"WG","off":"S0"}
    code+= flags[data["set_mode"]]
    

    
    #set_timer = str(data["set_timer"]).split(":")
    #operate_minute = (int(set_timer[0]) * 60) + int(set_timer[1])
    #operate_second = int(set_timer[2])
    operate_minute = data["set_min"]
    operate_second = 0 
    code += chr((data['set_infra1'] // 10) + 48)
    code += chr((data['set_infra2'] // 10) + 48)
    
    code += pad(2,data['set_temperature'],)

    code += pad(2,(operate_minute // 256))
    code += pad(2,(operate_minute % 256))
    code += pad(2,(operate_second))

    light_dec = 0
    if data['light']: light_dec += 0x01
    if data['mood_light']: light_dec += 0x02
    if data['starry_sky']: light_dec += 0x04
    if data['salt_wall']: light_dec += 0x08
    if data['air']: light_dec += 0x10
    #if data['operateend'] in ['operateend2', 'operateend3']: light_dec += 0x20
    code += chr(light_dec + 48)

    code += '000000'  # measured temperature, steam, fan time
    code += pad(2,(data["steam_on"]))
    code += '01'  # fan time, sauna status

    # Hardware version handling (similar to JS)
    if data['hwversion'] > 0:
        floor_temp = data['floorheattemp'] + 50 if "floorheaton" in data else data['floorheattemp']
        code += pad(2,floor_temp)
        code += pad(2,data['floortemp'])
        code += '00'

    
    code += "3" # hw version 3
    code += "ajlpybvmb"

    return code

"""data["set_infra1"] = 80

data["set_temperature"] = 60
data["set_timer"] = "00:50:00"
data["set_mode"] = "infra"
data["light"] = True
res = encode_setting()
print(res)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(res.encode())

"""
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
    client.subscribe("isauna/data")
    
def on_disconnect(client:Client, userdata, flags, rc, *args):
    print(f"Dissconected {rc}")
   

on_disconnect