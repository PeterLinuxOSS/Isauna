# iSauna Home Assistant Integration

![iSauna icon](assets/icon.webp)

A native Home Assistant integration for iSauna sauna controllers.

## What it does

- Integrates iSauna as a native Home Assistant device
- Supports climate, sensor, switch, number, and select entities
- Polls the sauna locally over the network
- Applies control changes automatically with debounce
- No MQTT broker or external add-on required

## Installation

1. Copy `custom_components/isauna` into `config/custom_components/isauna`
2. Restart Home Assistant
3. Go to **Settings → Devices & Services → Add Integration → iSauna**
4. Enter the controller host/IP and save

## Repository structure

```
custom_components/isauna/
├── manifest.json
├── __init__.py
├── config_flow.py
├── const.py
├── device.py
├── coordinator.py
├── entity.py
├── climate.py
├── sensor.py
├── switch.py
├── number.py
├── select.py
├── protocol.py
├── strings.json
└── translations/en.json
```

## HACS

This repository is prepared for HACS with `hacs.json` and a standard custom
integration layout.

To add it to HACS:

1. Open Home Assistant and go to **HACS → Integrations**
2. Choose **Explore & add repositories**
3. Add this repository URL as a custom repository of category **Integration**
4. Install the integration and restart Home Assistant
