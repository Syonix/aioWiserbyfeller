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
    UNIT_TEMPERATURE_CELSIUS,
)
from .errors import InvalidArgument
from .map import DEVICE_A_BLOCK_FWID_BLOCK_MAP, DEVICE_A_BLOCK_HWID_MAP


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


def parse_wiser_device_hwid_a(value: str) -> dict[str, int | None]:
    """Parse a Feller Wiser A block hardware ID.

    The A block hardware ID (self.a["hw_id"]) is a bit field of 2 bytes.
    Those bytes contain four values: type, features, channels and a hardware revision.

    +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    |  0 | channels 0-4 |   channel_type    |  channel_features |   hw_revision     |
    +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    Source: http://{µGW host}/kPlus/lib.js

    Examples:
        Type=4, Features=1, Channels=6 is the heating valve controller with 6 channels.
        Type=4, Features=0, Channels=0 is the room temperature sensor.

    This helper function breaks out each value into a dict.

    """
    result = {
        "revision": None,
        "features": None,
        "type": None,
        "channels": 0,
    }

    try:
        value = int(value, 16)
    except ValueError:
        return result

    result["revision"] = value & 0x0F
    result["features"] = (value >> 4) & 0x0F
    result["type"] = (value >> 8) & 0x0F
    result["channels"] = (value >> 12) & 0x0F

    return result


def parse_wiser_device_fwid(value: str) -> dict[str, int | None]:
    """Parse a Feller Wiser device firmware ID.

    The Wiser device firmware ID (self.a["hw_id"]) is a bit field of 2 bytes.
    Depending on the device type (A block or C block) it contains different information:

    C block
    +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    | 1  |           hw_type           |                        |   fw_revision     |
    +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+

    A block
    +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    | 0  |              |   channel_type    |  channel_features |   fw_revision     |
    +----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+----+
    Source: http://{µGW host}/kPlus/lib.js

    This helper function breaks out each value into a dict.
    """

    result = {
        "block_type": None,
        "revision": None,
    }

    try:
        value = int(value, 16)
    except ValueError:
        return result

    is_c_block = value & 0x8000
    result["block_type"] = "C" if is_c_block else "A"
    result["revision"] = value & 0x0F

    if is_c_block:
        result["hw_type"] = (value >> 9) & 0x3F
    else:
        result["channel_type"] = (value >> 8) & 0x0F
        result["channel_features"] = (value >> 4) & 0x0F

    return result


def get_device_name_by_hwid_a(value: str | None) -> str:
    """Return device name by hardware ID."""
    best_match = "Unknown"

    if value in (None, ""):
        return best_match

    info = parse_wiser_device_hwid_a(value)
    for entry in DEVICE_A_BLOCK_HWID_MAP:
        if entry["type"] == info["type"]:
            if entry["feature"] == info["features"]:
                best_match = entry["name"]
                break  # Exact match
            if entry["feature"] is None:
                best_match = entry["name"]  # Temporarily set, but continue searching

    return best_match + (f" {info['channels']}K" if info["channels"] != 0x0 else "")


def get_device_name_by_fwid(
    value: str | None, include_block_suffix: bool = False
) -> str:
    """Return device name by firmware ID."""
    if value in (None, ""):
        return "Unknown"

    fw_id = int(value, 16)
    b = (
        DEVICE_A_BLOCK_FWID_BLOCK_MAP[0]
        if (fw_id & 0x8000)
        else DEVICE_A_BLOCK_FWID_BLOCK_MAP[1]
    )

    for map_fwid, name in b["fw_id_map"].items():
        if (map_fwid & b["mask"]) == (fw_id & b["mask"]):
            suffix = b["main_name"] if include_block_suffix else ""
            return f"{name} {suffix}".strip()

    return "Unknown"


def normalize_unit(value):
    """Normalize unit values from the API."""
    match value:
        case "℃" | "C":
            return UNIT_TEMPERATURE_CELSIUS
        case _:
            return value
