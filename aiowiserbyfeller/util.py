"""Various helpers."""

from __future__ import annotations

from .const import (
    DEVICE_A_TYPE_DIMMER_DALI,
    DEVICE_A_TYPE_DIMMER_LED,
    DEVICE_A_TYPE_HVAC,
    DEVICE_A_TYPE_MOTOR,
    DEVICE_A_TYPE_NOOP,
    DEVICE_A_TYPE_SWITCH,
    DEVICE_A_TYPE_WEATHER_STATION,
    DEVICE_A_TYPE_WEATHER_STATION_REG,
    DEVICE_C_TYPE_DIMMER,
    DEVICE_C_TYPE_HVAC,
    DEVICE_C_TYPE_MOTOR,
    DEVICE_C_TYPE_SCENE,
    DEVICE_C_TYPE_SENSOR_TEMPERATURE,
    DEVICE_C_TYPE_SWITCH,
    DEVICE_C_TYPE_WEATHER_STATION,
    DEVICE_C_TYPE_WEATHER_STATION_REG,
    DEVICE_GENERATION_A,
    DEVICE_GENERATION_B,
)
from .errors import InvalidArgument


def validate_str(value, valid, **kwargs):
    """Validate a string by checking it against list ofr valid values."""
    error = kwargs.get("error_message", "Invalid value")

    if value not in valid:
        valid = ", ".join(valid)
        valid_str = f" Valid values: {valid}" if valid else ""
        raise InvalidArgument(f"{error} {value}.{valid_str}")


def parse_wiser_device_ref_c(value: str) -> dict:
    """Parse a Feller Wiser control (Bedienaufsatz) product reference."""
    result = {
        "type": None,
        "wlan": ".W" in value,
        "scene": 0,
        "loads": 0,
        "sensors": 0,
        "generation": None,
    }

    if ".VS" in value:
        result["scene"] = 2
    elif ".S4" in value:
        result["scene"] = 4
    elif ".S" in value or ".S1" in value:
        result["scene"] = 1

    if "3400" in value:
        result["type"] = DEVICE_C_TYPE_SCENE
    elif "3404" in value or "3405" in value:
        result["type"] = DEVICE_C_TYPE_MOTOR
    elif "3406" in value or "3407" in value:
        result["type"] = DEVICE_C_TYPE_DIMMER
    elif "3401" in value or "3402" in value:
        result["type"] = DEVICE_C_TYPE_SWITCH
    elif "3440" in value and ".MS" in value:
        result["type"] = DEVICE_C_TYPE_WEATHER_STATION
    elif "3440" in value and ".REG" in value:
        result["type"] = DEVICE_C_TYPE_WEATHER_STATION_REG
    elif "3470" in value and ".HK" in value:
        result["type"] = DEVICE_C_TYPE_HVAC
    elif "3475" in value and ".T1" in value:
        result["type"] = DEVICE_C_TYPE_SENSOR_TEMPERATURE

    if "3401" in value or "3406" in value or "3404" in value:
        result["loads"] = 1
    elif "3402" in value or "3405" in value or "3407" in value:
        result["loads"] = 2
    elif "3470" in value and ".6." in value:
        result["loads"] = 6

    if "3440" in value and ".MS" in value:
        result["sensors"] = 4
    elif "3475" in value and ".T1" in value:
        result["sensors"] = 1

    if ".A." in value or value.endswith(".A"):
        result["generation"] = DEVICE_GENERATION_A
    elif ".B." in value or value.endswith(".B"):
        result["generation"] = DEVICE_GENERATION_B

    return result


def parse_wiser_device_ref_a(value: str) -> dict:
    """Parse a Feller Wiser actuator (Funktionseinsatz) product reference."""
    result = {"loads": 0, "generation": None}

    if "3400" in value:
        result["type"] = DEVICE_A_TYPE_NOOP
    elif "3401" in value or "3402" in value:
        result["type"] = DEVICE_A_TYPE_SWITCH
    elif "3404" in value or "3405" in value:
        result["type"] = DEVICE_A_TYPE_MOTOR
    elif "3406" in value or "3407" in value:
        result["type"] = DEVICE_A_TYPE_DIMMER_LED
    elif "3411" in value:
        result["type"] = DEVICE_A_TYPE_DIMMER_DALI
    elif "3440" in value and ".MS" in value:
        result["type"] = DEVICE_A_TYPE_WEATHER_STATION
    elif "3440" in value and ".REG" in value:
        result["type"] = DEVICE_A_TYPE_WEATHER_STATION_REG
    elif "3470" in value and ".HK" in value:
        result["type"] = DEVICE_A_TYPE_HVAC

    if "3401" in value or "3404" in value or "3406" in value or "3411" in value:
        result["loads"] = 1
    elif "3402" in value or "3405" in value or "3407" in value:
        result["loads"] = 2
    elif "3470" in value and ".6." in value:
        result["loads"] = 6

    if ".A." in value or value.endswith(".A"):
        result["generation"] = DEVICE_GENERATION_A
    elif ".B." in value or value.endswith(".B"):
        result["generation"] = DEVICE_GENERATION_B

    return result


def parse_wiser_device_hwid_a(value: str) -> str:
    """Parse a Feller Wiser actuator (Funktionseinsatz) hardware id."""
    a_block_map = [
        {"name": "NS", "type": 0x0, "feature": None},
        {"name": "ONOFF", "type": 0x1, "feature": None},
        {"name": "DIMMER", "type": 0x2, "feature": None},
        {"name": "MOTOR", "type": 0x3, "feature": None},
        {"name": "THERMOSTAT", "type": 0x4, "feature": None},
        {"name": "VALVE CONTROLLER", "type": 0x4, "feature": 0x1},
        {"name": "DALI", "type": 0x2, "feature": 0x1},
        {"name": "WEATHER STATION", "type": 0x0, "feature": 0x4},
    ]
    if value in (None, ""):
        return "UNKNOWN"

    value = int(value, 16)
    channel_type = (value >> 8) & 0x0F
    channel_features = (value >> 4) & 0x0F
    channels = (value >> 12) & 0x07
    best_match = "UNKNOWN"
    for entry in a_block_map:
        if entry["type"] == channel_type:
            if entry["feature"] == channel_features:
                best_match = entry["name"]
                break  # Exact match
            if entry["feature"] is None:
                best_match = entry["name"]  # Temporarily set, but continue searching
    return best_match + (f" {channels}K" if channels != 0x0 else "")


def parse_wiser_device_fwid(value: str) -> str:
    """Parse a Feller Wiser device firmware id."""
    if value in (None, ""):
        return "Unknown"

    c_block_map = {
        0x8402: "Button-Front",
        0x8600: "microGW Button-Front",
        0x9000: "Sensor-Front",
        0x9200: "Display-Front",
        0xA000: "WEST-Interface",
        0xAA00: "Valve-Controller",
        0xBA00: "Push-Button-Interface",
        0xC000: "DinRailGW",
    }
    a_block_map = {
        0x0100: "OnOff/NS",
        0x0200: "RLRC-Dimmer",
        0x0210: "DALI-Dimmer",
        0x0220: "10V-Dimmer",
        0x0300: "Motor",
        0x0400: "Thermostat",
        0x0410: "Valve-Controller",
    }
    block_map = [
        {
            "mask": 0x7E00,
            "main_name": "C-Block",
            "fw_id_map": c_block_map,
        },
        {
            "mask": 0xFF0,
            "main_name": "A-Block",
            "fw_id_map": a_block_map,
        },
    ]
    fw_id = int(value, 16)
    b = block_map[0] if (fw_id & 0x8000) else block_map[1]

    for map_fwid, name in b["fw_id_map"].items():
        if (map_fwid & b["mask"]) == (fw_id & b["mask"]):
            return f"{name} {b['main_name']}"
    return "Unknown"
