HOST = "10.10.111.2"
temperature_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",
        },
        {
            "topic": "isauna/data",
            "value_template": "{{ value_json.temperaturerror }}",
            "payload_available": False,
            "payload_not_available": True
        }
    ],
    "availability_mode": "all",

    "device_class": "temperature",
    "state_topic": "isauna/data",
    "unit_of_measurement": "°C",
    "value_template": "{{ value_json.currentsaunatemp}}",
    "unique_id": "isauna_temperature",
    "device": {
        "identifiers": [
            "isauna"
        ],
        "name": "iSauna",
        "manufacturer": "iSauna Home",
        "model": "Basic",
        "serial_number": "12AE3010545",
        "hw_version": "1.01",
        "sw_version": "2024.1.0",
        "configuration_url": f"http://{HOST}/"
    }
}


humidity_template = {

    "availability": [
        {
            "topic": "isauna/bridge/state",

        },
        {
            "topic": "isauna/data",
            "value_template": "{{ value_json.steamerror }}",
            "payload_available": False,
            "payload_not_available": True

        }
    ],
    "availability_mode": "all",
    "device_class": "humidity",
    "state_topic": "isauna/data",
    "unit_of_measurement": "%",
    "value_template": "{{ value_json.currentsteam}}",
    "unique_id": "isauna_humidity",
    "device": {
        "identifiers": [
            "isauna"
        ]
    }
}
desired_temperature_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],

    "device_class": "temperature",
    "name": "Desired Temperature",
    "state_topic": "isauna/data",
    "unit_of_measurement": "°C",
    "value_template": "{{ value_json.desired_temperature}}",
    "unique_id": "isauna_desired_temperature",
    "device": {
        "identifiers": [
            "isauna"
        ]
    }
}

mode_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],

    "name": "Mode",
    "state_topic": "isauna/data",
    "value_template": "{{ value_json.mode}}",
    "unique_id": "isauna_mode",
    "device": {
        "identifiers": [
            "isauna"
        ]
    }
}

infra1_template = {

    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Infra Fill 1",
    "availability_mode": "all",
    "state_topic": "isauna/data",
    "unit_of_measurement": "%",
    "value_template": "{{ value_json.infra1}}",
    "unique_id": "isauna_infra1",
    "device": {
        "identifiers": [
            "isauna"
        ]
    }
}
infra2_template = {

    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Infra Fill 2",
    "availability_mode": "all",
    "state_topic": "isauna/data",
    "unit_of_measurement": "%",
    "value_template": "{{ value_json.infra2}}",
    "unique_id": "isauna_infra2",
    "device": {
        "identifiers": [
            "isauna"
        ]
    }
}
timer_template = {

    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Timer",
    "availability_mode": "all",
    "state_topic": "isauna/data",
    "value_template": "{{ value_json.timer}}",
    "unique_id": "isauna_timer",
    "device": {
        "identifiers": [
            "isauna"
        ]
    }
}
airtimer_template = {

    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Air Timer",
    "availability_mode": "all",
    "state_topic": "isauna/data",
    "value_template": "{{ value_json.airtimer}}",
    "unique_id": "isauna_airtimer",
    "device": {
        "identifiers": [
            "isauna"
        ]
    }
}

light_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Light",
    "command_topic": "homeassistant/switch/isauna/light/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.light}}",
    "state_on": True,
    "state_off": False,
    "payload_off":0,
    "payload_on":1,
    "unique_id": "isauna_light",
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}

mood_light_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Mood Light",
    "command_topic": "homeassistant/switch/isauna/mood_light/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.mood_light}}",
    "state_on": True,
    "state_off": False,
    "payload_off":0,
    "payload_on":1,
    "unique_id": "mood_light",
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}

starry_sky_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Starry Sky",
    "command_topic": "homeassistant/switch/isauna/starry_sky/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.starry_sky}}",
    "state_on": True,
    "state_off": False,
    "payload_off":0,
    "payload_on":1,
    "unique_id": "starry_sky",
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}

air_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Air",
    "command_topic": "homeassistant/switch/isauna/air/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.air}}",
    "state_on": True,
    "state_off": False,
    "payload_off":0,
    "payload_on":1,
    "unique_id": "air",
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}

set_infra1_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Infra 1",
    "command_topic": "homeassistant/number/isauna/set_infra1/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.set_infra1}}",

    "unique_id": "set_infra1",
    "device_class":"power_factor",
    "min":0,
    "max":100,
    "step":10,
    "mode":"slider",
    "unit_of_measurement":"%",
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}

set_infra2_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Infra 2",
    "command_topic": "homeassistant/number/isauna/set_infra2/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.set_infra2}}",
    "unique_id": "set_infra2",
    "device_class":"power_factor",
    "min":0,
    "max":100,
    "step":10,
    "mode":"slider",
    "unit_of_measurement":"%",
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}

update_button_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Update Button",
    "command_topic": "homeassistant/button/isauna/update_button/set",
    "payload_press":"PRESS",
  
    
    
    "unique_id": "update_button",
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}


set_mode_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Set Mode",
    "command_topic": "homeassistant/select/isauna/set_mode/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.set_mode}}",
    "unique_id": "set_mode",
    "options":[
        "off","infra","finn","steam",
    ],
    
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}

set_temperature_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Set Temperature",
    "command_topic": "homeassistant/number/isauna/set_temperature/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.set_temperature}}",
    "unique_id": "set_temperature",
    "device_class":"temperature",
    "min":30,
    "max":120,
    "mode":"slider",
    "unit_of_measurement":"°C",
    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}

set_min_template = {
    "availability": [
        {
            "topic": "isauna/bridge/state",

        },

    ],
    "name": "Set Minutes",
    "command_topic": "homeassistant/number/isauna/set_min/set",

    "state_topic": "isauna/data",
    "value_template": "{{ value_json.set_min}}",
    "unique_id": "set_min",
    "unit_of_measurement":"min/s",
    "mode":"box",
    

    "device": {
        "identifiers": [
            "isauna"
        ]

    }
}