"""Various helpers."""
from __future__ import annotations

from .errors import InvalidArgument


def validate_str(value, valid, **kwargs):
    """Validate a string by checking it against list ofr valid values"""
    error = kwargs.get("error_message", "Invalid value")

    if value not in valid:
        valid = ", ".join(valid)
        valid_str = f" Valid values: {valid}" if valid else ""
        raise InvalidArgument(f"{error} {value}.{valid_str}")


def parse_wiser_device_ref_c(value: str) -> dict:
    """Parse a Feller Wiser control front (Bedienaufsatz) product
    reference"""
    result = {
        "type": None,
        "wlan": ".W" in value,
        "scene": 0,
        "loads": 0,
        "generation": None,
    }

    if "VS" in value:
        result["scene"] = 2
    elif "S4" in value:
        result["scene"] = 4
    elif "S" in value or "S1" in value:
        result["scene"] = 1

    if "3400" in value:
        result["type"] = "scene"
    elif "3404" in value or "3405" in value:
        result["type"] = "motor"
    elif "3406" in value or "3407" in value:
        result["type"] = "dimmer"
    elif "3401" in value or "3402" in value:
        result["type"] = "switch"

    if "3401" in value or "3406" in value or "3404" in value:
        result["loads"] = 1
    elif "3402" in value or "3405" in value or "3407" in value:
        result["loads"] = 2

    if ".A." in value or value.endswith(".A"):
        result["generation"] = "A"
    elif ".B." in value or value.endswith(".B"):
        result["generation"] = "B"

    return result


def parse_wiser_device_ref_a(value: str) -> dict:
    """Parse a Feller Wiser base module (Funktionseinsatz) product
    reference"""
    result = {"loads": 0, "generation": None}

    if "3400" in value:
        result["type"] = "noop"
    elif "3401" in value or "3402" in value:
        result["type"] = "switch"
    elif "3404" in value or "3405" in value:
        result["type"] = "motor"
    elif "3406" in value or "3407" in value:
        result["type"] = "dimmer-led"
    elif "3411" in value:
        result["type"] = "dimmer-dali"

    if "3401" in value or "3404" in value or "3406" in value or "3411" in value:
        result["loads"] = 1
    elif "3402" in value or "3405" in value or "3407" in value:
        result["loads"] = 2

    if ".A." in value:
        result["generation"] = "A"
    elif ".B." in value:
        result["generation"] = "B"

    return result
