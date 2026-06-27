"""Pure encode/decode helpers for the iSauna controller protocol.

These functions contain no I/O and no Home Assistant dependencies so they can be
unit-tested in isolation. They were ported from the original MQTT bridge.
"""

from __future__ import annotations

from .const import CHARS_TO_REMOVE, DECODE_MODE_FLAGS, ENCODE_MODE_FLAGS


class IsaunaProtocolError(Exception):
    """Raised when a controller response cannot be decoded."""


def remove_chars(text: str, chars: list[str]) -> str:
    """Strip the controller's framing characters from a payload."""
    for char in chars:
        text = text.replace(char, "")
    return text


def _pad_hex(width: int, value: int | str, padding: str = "0") -> str:
    """Encode an int (or string) as lower-case hex, left-padded to ``width``."""
    if isinstance(value, int):
        encoded = format(value, "x")
    elif isinstance(value, str):
        encoded = "".join(format(ord(c), "x") for c in value)
    else:
        raise TypeError(f"Unsupported input type for pad: {type(value)}")
    return padding * (width - len(encoded)) + encoded


def decode_state(result: str, hwversion: int = 0) -> dict | None:
    """Decode a raw controller payload into a state dict.

    Returns ``None`` when the payload is merely the echo of our read command
    (it starts with ``c``) and therefore carries no new state.
    """
    if not result or result.startswith("c"):
        return None

    if len(result) < 24:
        raise IsaunaProtocolError(f"payload too short: {result!r}")

    data: dict = {}
    try:
        data["mode"] = DECODE_MODE_FLAGS[result[2]]
        data["desired_temperature"] = int(result[5:7], 16)

        data["infra1"] = (ord(result[3]) - 48) * 10
        data["infra2"] = (ord(result[4]) - 48) * 10

        minutes = int(result[7:9], 16) * 256 + int(result[9:11], 16)
        data["timer"] = f"{minutes // 60}:{minutes % 60}:{int(result[11:13], 16)}"

        light_dec = ord(result[13]) - 48
        data["light"] = bool(light_dec & 0x01)
        data["mood_light"] = bool(light_dec & 0x02)
        data["starry_sky"] = bool(light_dec & 0x04)
        data["salt_wall"] = bool(light_dec & 0x08)
        data["air"] = bool(light_dec & 0x10)

        current_temp = int(result[14:16], 16)
        data["temperaturerror"] = current_temp == 255
        data["currentsaunatemp"] = current_temp

        current_steam = int(result[16:18], 16)
        data["steamerror"] = current_steam == 255
        data["currentsteam"] = current_steam
        data["steam"] = int(result[20:22], 16)

        air_time = ord(result[22]) - 48
        data["airtimer"] = f"{air_time // 60}:{air_time % 60}:{ord(result[18]) - 48}"

        data["watererror"] = False
        if data["mode"] == "steam" and len(result) > 23:
            data["watererror"] = result[23]

        if hwversion > 0 and len(result) >= 30:
            data["floorheatcurtemp"] = int(result[28:30], 16)
            data["floorheaterror"] = data["floorheatcurtemp"] == 255
            floor_temp = int(result[24:26], 16)
            if floor_temp < 40:
                data["floorheaton"] = False
            else:
                data["floorheatemp"] = floor_temp - 50
                data["floorheaton"] = True
            data["temperaltemp"] = int(result[26:28], 16)
    except (KeyError, ValueError, IndexError) as err:
        raise IsaunaProtocolError(f"failed to decode {result!r}: {err}") from err

    return data


def decode_response(raw: bytes, hwversion: int = 0) -> dict | None:
    """Validate an HTTP response and decode its payload line."""
    lines = raw.decode("utf-8", errors="ignore").splitlines()
    if not lines or lines[0] != "HTTP/1.1 200 OK":
        raise IsaunaProtocolError("controller did not return HTTP 200")
    result = remove_chars(lines[-1], CHARS_TO_REMOVE)
    return decode_state(result, hwversion)


def encode_settings(data: dict, password: str) -> str:
    """Encode a state dict into the controller's write command."""
    try:
        code = "$$$AC" + ENCODE_MODE_FLAGS[data["set_mode"]]

        operate_minute = int(data["set_min"])
        operate_second = 0

        code += chr((data["set_infra1"] // 10) + 48)
        code += chr((data["set_infra2"] // 10) + 48)
        code += _pad_hex(2, int(data["set_temperature"]))
        code += _pad_hex(2, operate_minute // 256)
        code += _pad_hex(2, operate_minute % 256)
        code += _pad_hex(2, operate_second)

        light_dec = 0
        if data.get("light"):
            light_dec += 0x01
        if data.get("mood_light"):
            light_dec += 0x02
        if data.get("starry_sky"):
            light_dec += 0x04
        if data.get("salt_wall"):
            light_dec += 0x08
        if data.get("air"):
            light_dec += 0x10
        code += chr(light_dec + 48)

        code += "000000"  # measured temperature, steam, fan time
        code += _pad_hex(2, data.get("steam_on", 0))
        code += "01"  # fan time, sauna status

        if data.get("hwversion", 0) > 0:
            floor_temp = (
                data["floorheattemp"] + 50
                if data.get("floorheaton")
                else data["floorheattemp"]
            )
            code += _pad_hex(2, floor_temp)
            code += _pad_hex(2, data["floortemp"])
            code += "00"

        code += "3"  # hw version 3
        code += password
    except (KeyError, ValueError, TypeError) as err:
        raise IsaunaProtocolError(f"failed to encode settings: {err}") from err

    return code
