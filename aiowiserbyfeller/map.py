"""Various mappings."""

# Maps the hw_id to A block
DEVICE_A_BLOCK_HWID_MAP = [
    {"name": "Secondary Control", "type": 0x0, "feature": None},
    {"name": "On/Off", "type": 0x1, "feature": None},
    {"name": "Dimmer", "type": 0x2, "feature": None},
    {"name": "Motor", "type": 0x3, "feature": None},
    {"name": "Thermostat", "type": 0x4, "feature": None},
    {"name": "Valve Controller", "type": 0x4, "feature": 0x1},
    {"name": "Dali", "type": 0x2, "feature": 0x1},
    {"name": "Weather Station", "type": 0x0, "feature": 0x4},
]

# Maps the fw_id to C block
DEVICE_C_BLOCK_FWID_MAP = {
    0x8402: "Button Front",
    0x8600: "µGateway Button Front",
    0x9000: "Sensor Front",
    0x9200: "Display Front",
    0xA000: "Weather Station",
    0xAA00: "Valve Controller",
    0xBA00: "Push Button Interface",
    0xC000: "DIN Rail Gateway",
}

# Maps the fw_id to A block
DEVICE_A_BLOCK_FWID_MAP = {
    0x0100: "On/Off / Secondary Control",
    0x0200: "RL/RC Dimmer",
    0x0210: "DALI Dimmer",
    0x0220: "10V Dimmer",
    0x0300: "Motor",
    0x0400: "Thermostat",
    0x0410: "Valve Controller",
}

# Combines the fw_id maps for A and C blocks
DEVICE_A_BLOCK_FWID_BLOCK_MAP = [
    {
        "mask": 0x7E00,
        "main_name": "C-Block",
        "fw_id_map": DEVICE_C_BLOCK_FWID_MAP,
    },
    {
        "mask": 0xFF0,
        "main_name": "A-Block",
        "fw_id_map": DEVICE_A_BLOCK_FWID_MAP,
    },
]

# Fields that are required when validating device data
DEVICE_CHECK_FIELDS = {
    "c": ["comm_ref", "fw_version", "comm_name", "serial_nr"],
    "a": ["comm_ref", "fw_version", "comm_name", "serial_nr"],
}

# Fields that are allowed to be empty for specific device types.
# Keys can be a combination of hwid type and hwid feature flag or specific hardware ids.
DEVICE_ALLOWED_EMPTY_FIELDS = {
    0x41: {"c": ["serial_nr"], "a": []},
    0x4: {"c": ["serial_nr"], "a": []},
}
