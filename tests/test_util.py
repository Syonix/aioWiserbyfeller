"""aiowiserbyfeller util tests."""

import pytest

from aiowiserbyfeller import InvalidArgument
from aiowiserbyfeller.util import (
    get_device_name_by_fwid,
    get_device_name_by_hwid_a,
    parse_wiser_device_fwid,
    parse_wiser_device_hwid_a,
    parse_wiser_device_ref_a,
    parse_wiser_device_ref_c,
    validate_str,
)


def validate_str_data_valid() -> list[str]:
    """Provide data for test_validate_str_valid."""
    return ["valid", "ok", "good"]


def ref_c_data() -> list[list]:
    """Provide data for test_parse_wiser_device_ref_c."""
    return [
        # -- Bedienaufsätze ohne WLAN ----------------------------------
        [
            # Bedienaufsatz Wiser Szenentaster 1 Szene
            "926-3400.1.S1.A",
            {
                "type": "scene",
                "wlan": False,
                "scene": 1,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Szenentaster 2 Szenen vertikal
            "926-3400.2.VS.A",
            {
                "type": "scene",
                "wlan": False,
                "scene": 2,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Szenentaster 4 Szenen
            "926-3400.4.S4.A",
            {
                "type": "scene",
                "wlan": False,
                "scene": 4,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 1-Kanal
            "926-3401.1.A",
            {
                "type": "switch",
                "wlan": False,
                "scene": 0,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 1-Kanal Szene
            "926-3401.2.S1.A",
            {
                "type": "switch",
                "wlan": False,
                "scene": 1,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 2-Kanal
            "926-3402.2.A",
            {
                "type": "switch",
                "wlan": False,
                "scene": 0,
                "loads": 2,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 1-Kanal
            "926-3404.2.A",
            {
                "type": "motor",
                "wlan": False,
                "scene": 0,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 1-Kanal Szene
            "926-3404.4.S.A",
            {
                "type": "motor",
                "wlan": False,
                "scene": 1,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 2-Kanal
            "926-3405.4.A",
            {
                "type": "motor",
                "wlan": False,
                "scene": 0,
                "loads": 2,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Dimmer 1-Kanal
            "926-3406.2.A",
            {
                "type": "dimmer",
                "wlan": False,
                "scene": 0,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Dimmer 1-Kanal Szene
            "926-3406.4.S.A",
            {
                "type": "dimmer",
                "wlan": False,
                "scene": 1,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Dimmer 2-Kanal
            "926-3407.4.A",
            {
                "type": "dimmer",
                "wlan": False,
                "scene": 0,
                "loads": 2,
                "sensors": 0,
                "generation": "A",
            },
        ],
        # -- Bedienaufsätze mit WLAN -----------------------------------
        [
            # Bedienaufsatz Wiser Szenentaster 1 Szene WLAN Gen.A
            "926-3400.1.S1.W.A",
            {
                "type": "scene",
                "wlan": True,
                "scene": 1,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Szenentaster 2 Szenen vertikal WLAN Gen.A
            "926-3400.2.VS.W.A",
            {
                "type": "scene",
                "wlan": True,
                "scene": 2,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Szenentaster 4 Szenen WLAN Gen.A
            "926-3400.4.S4.W.A",
            {
                "type": "scene",
                "wlan": True,
                "scene": 4,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 1-Kanal WLAN Gen.A
            "926-3401.1.W.A",
            {
                "type": "switch",
                "wlan": True,
                "scene": 0,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 1-Kanal Szene WLAN Gen.A
            "926-3401.2.S1.W.A",
            {
                "type": "switch",
                "wlan": True,
                "scene": 1,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 2-Kanal WLAN Gen.A
            "926-3402.2.W.A",
            {
                "type": "switch",
                "wlan": True,
                "scene": 0,
                "loads": 2,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 1-Kanal WLAN Gen.A
            "926-3404.2.W.A",
            {
                "type": "motor",
                "wlan": True,
                "scene": 0,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 1-Kanal Szene WLAN Gen.A
            "926-3404.4.S.W.A",
            {
                "type": "motor",
                "wlan": True,
                "scene": 1,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 2-Kanal WLAN Gen.A
            "926-3405.4.W.A",
            {
                "type": "motor",
                "wlan": True,
                "scene": 0,
                "loads": 2,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Dimmer 1-Kanal WLAN Gen.A
            "926-3406.2.W.A",
            {
                "type": "dimmer",
                "wlan": True,
                "scene": 0,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Dimmer 1-Kanal Szene WLAN Gen.A
            "926-3406.4.S.W.A",
            {
                "type": "dimmer",
                "wlan": True,
                "scene": 1,
                "loads": 1,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Dimmer 2-Kanal WLAN Gen.A
            "926-3407.4.W.A",
            {
                "type": "dimmer",
                "wlan": True,
                "scene": 0,
                "loads": 2,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # Bedienaufsatz Wiser Dimmer 2-Kanal WLAN Gen.B
            "926-3407.4.W.B",
            {
                "type": "dimmer",
                "wlan": True,
                "scene": 0,
                "loads": 2,
                "sensors": 0,
                "generation": "B",
            },
        ],
        # -- Full assembly numbers --------------------------------------------
        # (not reported by Wiser API but available in webshop)
        [
            # Bedienaufsatz Wiser Dimmer 2-Kanal WLAN Gen.B
            "926-3407.4.W.B.FMI.61",
            {
                "type": "dimmer",
                "wlan": True,
                "scene": 0,
                "loads": 2,
                "sensors": 0,
                "generation": "B",
            },
        ],
        [
            # EDIZIOdue Bedienaufsatz Wiser Szenentaster 1 Szene WLAN Gen.A
            "926-3400.1.S1.W.A.FMI.61",
            {
                "type": "scene",
                "wlan": True,
                "scene": 1,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # EDIZIOdue Bedienaufsatz Wiser Szenentaster 1 Szene WLAN Gen.B
            "926-3400.1.S1.W.B.FMI.61",
            {
                "type": "scene",
                "wlan": True,
                "scene": 1,
                "loads": 0,
                "sensors": 0,
                "generation": "B",
            },
        ],
        [
            # STANDARDdue Bedienaufsatz Wiser Szenentaster 1 Szene WLAN Gen.A
            "926-3400.1.S1.W.A.QMI.61",
            {
                "type": "scene",
                "wlan": True,
                "scene": 1,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # EDIZIO.liv Abdeckset Wiser Szenentaster 1 Szene
            "920-3400.1.S1.GMI.A.61",
            {
                "type": "scene",
                "wlan": False,
                "scene": 1,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # EDIZIO.liv Bedienaufsatz Wiser Szenentaster 1 Szene WLAN Gen.A
            "926-3400.1.S1.W.A.GMI.A.61",
            {
                "type": "scene",
                "wlan": True,
                "scene": 1,
                "loads": 0,
                "sensors": 0,
                "generation": "A",
            },
        ],
        [
            # EDIZIOdue Abdeckset Wiser Szenentaster 1 Szene
            "920-3400.1.S1.FMI.61",
            {
                "type": "scene",
                "wlan": False,
                "scene": 1,
                "loads": 0,
                "sensors": 0,
                "generation": None,
            },
        ],
        [
            # EDIZIO.liv Bedienaufsatz Wiser Raumtemperatursensor
            "926-3475.0.T1.A.G.A.61",
            {
                "type": "sensor-temp",
                "wlan": False,
                "scene": 0,
                "loads": 0,
                "sensors": 1,
                "generation": "A",
            },
        ],
        # -- Weather station --------------------------------------------------
        [
            # Wiser Kombisensor/Wetterstation
            "3440.A.4.MS",
            {
                "type": "weather-station",
                "wlan": False,
                "scene": 0,
                "loads": 0,
                "sensors": 4,
                "generation": "A",
            },
        ],
        [
            # Wiser Wetterstation REG-Modul
            "3440.B.1.REG",
            {
                "type": "weather-station-reg",
                "wlan": False,
                "scene": 0,
                "loads": 0,
                "sensors": 0,
                "generation": "B",
            },
        ],
        # -- Heating controller -----------------------------------------------
        [
            # Wiser Heizungskontroller 6K
            "3470.B.6.HK",
            {
                "type": "hvac",
                "wlan": False,
                "scene": 0,
                "loads": 6,
                "sensors": 0,
                "generation": "B",
            },
        ],
        [
            # Wiser Raumtemperatursensor
            "3475.0.T1.A",
            {
                "type": "sensor-temp",
                "wlan": False,
                "scene": 0,
                "loads": 0,
                "sensors": 1,
                "generation": "A",
            },
        ],
    ]


def ref_a_data() -> list[list]:
    """Provide data for test_parse_wiser_device_ref_a."""
    return [
        # -- EDIZIOdue --------------------------------------------------------
        ["3400.A.BSE", {"loads": 0, "type": "noop", "generation": "A"}],
        ["3400.B.BSE", {"loads": 0, "type": "noop", "generation": "B"}],
        ["3401.B.BSE", {"loads": 1, "type": "switch", "generation": "B"}],
        ["3402.B.BSE", {"loads": 2, "type": "switch", "generation": "B"}],
        ["3404.B.BSE", {"loads": 1, "type": "motor", "generation": "B"}],
        ["3405.B.BSE", {"loads": 2, "type": "motor", "generation": "B"}],
        ["3406.B.BSE", {"loads": 1, "type": "dimmer-led", "generation": "B"}],
        ["3407.B.BSE", {"loads": 2, "type": "dimmer-led", "generation": "B"}],
        ["3411.B.BSE", {"loads": 1, "type": "dimmer-dali", "generation": "B"}],
        # -- EDIZIO.liv / Snapfix ---------------------------------------------
        ["3400.B.BAE", {"loads": 0, "type": "noop", "generation": "B"}],
    ]


def fwid_data() -> list[list]:
    """Provide data for parse_wiser_device_fwid."""
    return [
        # Invalid
        ["not a hex number", {"block_type": None, "revision": None}],
        # C block
        ["0x8402", {"block_type": "C", "revision": 2, "hw_type": 2}],
        ["0x8600", {"block_type": "C", "revision": 0, "hw_type": 3}],
        ["0x9000", {"block_type": "C", "revision": 0, "hw_type": 8}],
        ["0x9200", {"block_type": "C", "revision": 0, "hw_type": 9}],
        ["0xA000", {"block_type": "C", "revision": 0, "hw_type": 16}],
        ["0xAA00", {"block_type": "C", "revision": 0, "hw_type": 21}],
        ["0xBA00", {"block_type": "C", "revision": 0, "hw_type": 29}],
        ["0xC000", {"block_type": "C", "revision": 0, "hw_type": 32}],
        # A block
        [
            "0x0100",
            {
                "block_type": "A",
                "revision": 0,
                "channel_type": 1,
                "channel_features": 0,
            },
        ],
        [
            "0x0200",
            {
                "block_type": "A",
                "revision": 0,
                "channel_type": 2,
                "channel_features": 0,
            },
        ],
        [
            "0x0210",
            {
                "block_type": "A",
                "revision": 0,
                "channel_type": 2,
                "channel_features": 1,
            },
        ],
        [
            "0x0220",
            {
                "block_type": "A",
                "revision": 0,
                "channel_type": 2,
                "channel_features": 2,
            },
        ],
        [
            "0x0300",
            {
                "block_type": "A",
                "revision": 0,
                "channel_type": 3,
                "channel_features": 0,
            },
        ],
        [
            "0x0400",
            {
                "block_type": "A",
                "revision": 0,
                "channel_type": 4,
                "channel_features": 0,
            },
        ],
        [
            "0x0410",
            {
                "block_type": "A",
                "revision": 0,
                "channel_type": 4,
                "channel_features": 1,
            },
        ],
    ]


def hwid_a_data() -> list[list]:
    """Provide data for parse_wiser_device_hwid_a."""
    return [
        [
            "not a hex number",
            {"revision": None, "features": None, "type": None, "channels": 0},
        ],
        ["0x0033", {"revision": 3, "features": 3, "type": 0, "channels": 0}],
        ["0x1113", {"revision": 3, "features": 1, "type": 1, "channels": 1}],
        ["0x1203", {"revision": 3, "features": 0, "type": 2, "channels": 1}],
        ["0x2203", {"revision": 3, "features": 0, "type": 2, "channels": 2}],
        ["0x1303", {"revision": 3, "features": 0, "type": 3, "channels": 1}],
        ["0x2303", {"revision": 3, "features": 0, "type": 3, "channels": 2}],
        ["0x6413", {"revision": 3, "features": 1, "type": 4, "channels": 6}],
        ["0x2212", {"revision": 2, "features": 1, "type": 2, "channels": 2}],
        ["0x0040", {"revision": 0, "features": 4, "type": 0, "channels": 0}],
        ["0x0400", {"revision": 0, "features": 0, "type": 4, "channels": 0}],
    ]


def fwid_name_data() -> list[list]:
    """Provide data for test_get_device_name_by_fwid."""
    return [
        ["0x8402", "Button Front", "C-Block"],
        ["0x8600", "µGateway Button Front", "C-Block"],
        ["0x9000", "Sensor Front", "C-Block"],
        ["0x9200", "Display Front", "C-Block"],
        ["0xA000", "Weather Station", "C-Block"],
        ["0xAA00", "Valve Controller", "C-Block"],
        ["0xBA00", "Push Button Interface", "C-Block"],
        ["0xC000", "DIN Rail Gateway", "C-Block"],
        ["0x0100", "On/Off / Secondary Control", "A-Block"],
        ["0x0200", "RL/RC Dimmer", "A-Block"],
        ["0x0210", "DALI Dimmer", "A-Block"],
        ["0x0220", "10V Dimmer", "A-Block"],
        ["0x0300", "Motor", "A-Block"],
        ["0x0400", "Thermostat", "A-Block"],
        ["0x0410", "Valve Controller", "A-Block"],
        ["", "Unknown", ""],
        [None, "Unknown", ""],
    ]


def hwid_a_name_data() -> list[list]:
    """Provide data for test_get_device_name_by_hwid_a."""
    return [
        ["0x0033", "Secondary Control"],
        ["0x1113", "On/Off 1K"],
        ["0x1203", "Dimmer 1K"],
        ["0x2203", "Dimmer 2K"],
        ["0x1303", "Motor 1K"],
        ["0x2303", "Motor 2K"],
        ["0x6413", "Valve Controller 6K"],
        ["0x2212", "Dali 2K"],
        ["0x0040", "Weather Station"],
        ["0x0400", "Thermostat"],
        ["", "Unknown"],
        [None, "Unknown"],
    ]


@pytest.mark.parametrize("check_val", validate_str_data_valid())
def test_validate_str_valid(check_val: list):
    """Test validate_str with valid values."""
    valid = ["valid", "ok", "good"]
    validate_str(check_val, valid)
    assert True


def test_validate_str_invalid():
    """Test validate_str with invalid values."""

    with pytest.raises(InvalidArgument) as ex:
        validate_str("invalid", ["valid", "ok", "good"])

    expected_error = "Invalid value invalid. Valid values: valid, ok, good"
    assert str(ex.value) == expected_error

    expected_error = "This is the error message invalid."
    with pytest.raises(InvalidArgument) as ex:
        validate_str("invalid", [], error_message="This is the error message")

    assert str(ex.value) == expected_error


@pytest.mark.parametrize("data", ref_c_data())
def test_parse_wiser_device_ref_c(data: list):
    """Test parse_wiser_device_ref_c."""
    actual = parse_wiser_device_ref_c(data[0])
    assert actual == data[1]


@pytest.mark.parametrize("data", ref_a_data())
def test_parse_wiser_device_ref_a(data: list):
    """Test parse_wiser_device_ref_a."""
    actual = parse_wiser_device_ref_a(data[0])
    assert actual == data[1]


@pytest.mark.parametrize("data", hwid_a_data())
def test_parse_wiser_device_hwid_a(data: list):
    """Test parse_wiser_device_hwid_a."""
    actual = parse_wiser_device_hwid_a(data[0])
    assert actual == data[1]


@pytest.mark.parametrize("data", fwid_data())
def test_parse_wiser_device_fwid(data: list):
    """Test parse_wiser_device_fwid."""
    actual = parse_wiser_device_fwid(data[0])
    assert actual == data[1]


@pytest.mark.parametrize("data", hwid_a_name_data())
def test_get_device_name_by_hwid_a(data: list):
    """Test get_device_name_by_hwid_a."""
    actual = get_device_name_by_hwid_a(data[0])
    assert actual == data[1]


@pytest.mark.parametrize("data", fwid_name_data())
def test_get_device_name_by_fwid(data: list):
    """Test get_device_name_by_fwid."""
    actual = get_device_name_by_fwid(data[0])
    assert actual == data[1]


@pytest.mark.parametrize("data", fwid_name_data())
def test_get_device_name_by_fwid_with_blocktype(data: list):
    """Test get_device_name_by_fwid with blocktype."""
    actual = get_device_name_by_fwid(data[0], include_block_suffix=True)
    assert actual == (data[1] + " " + data[2] if data[2] != "" else data[1])
