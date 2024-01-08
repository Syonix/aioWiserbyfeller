"""aiowiserbyfeller util tests"""
import pytest
from aiowiserbyfeller.util import (
    parse_wiser_device_ref_c,
    parse_wiser_device_ref_a,
    validate_str,
)
from aiowiserbyfeller import InvalidArgument


def validate_str_data_valid() -> list[str]:
    """Data provider for test_validate_str_valid"""
    return ["valid", "ok", "good"]


def ref_c_data() -> list[list]:
    """Data provider for test_parse_wiser_device_ref_c"""
    return [
        # -- Bedienaufsätze ohne WLAN ----------------------------------
        [
            # Bedienaufsatz Wiser Szenentaster 1 Szene
            "926-3400.1.S1.A",
            {"type": "scene", "wlan": False, "scene": 1, "loads": 0},
        ],
        [
            # Bedienaufsatz Wiser Szenentaster 2 Szenen vertikal
            "926-3400.2.VS.A",
            {"type": "scene", "wlan": False, "scene": 2, "loads": 0},
        ],
        [
            # Bedienaufsatz Wiser Szenentaster 4 Szenen
            "926-3400.4.S4.A",
            {"type": "scene", "wlan": False, "scene": 4, "loads": 0},
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 1-Kanal
            "926-3401.1.A",
            {"type": "switch", "wlan": False, "scene": 0, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 1-Kanal Szene
            "926-3401.2.S1.A",
            {"type": "switch", "wlan": False, "scene": 1, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 2-Kanal
            "926-3402.2.A",
            {"type": "switch", "wlan": False, "scene": 0, "loads": 2},
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 1-Kanal
            "926-3404.2.A",
            {"type": "motor", "wlan": False, "scene": 0, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 1-Kanal Szene
            "926-3404.4.S.A",
            {"type": "motor", "wlan": False, "scene": 1, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 2-Kanal
            "926-3405.4.A",
            {"type": "motor", "wlan": False, "scene": 0, "loads": 2},
        ],
        [
            # Bedienaufsatz Wiser Dimmer 1-Kanal
            "926-3406.2.A",
            {"type": "dimmer", "wlan": False, "scene": 0, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Dimmer 1-Kanal Szene
            "926-3406.4.S.A",
            {"type": "dimmer", "wlan": False, "scene": 1, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Dimmer 2-Kanal
            "926-3407.4.A",
            {"type": "dimmer", "wlan": False, "scene": 0, "loads": 2},
        ],
        # -- Bedienaufsätze mit WLAN -----------------------------------
        [
            # Bedienaufsatz Wiser Szenentaster 1 Szene WLAN Gen.A
            "926-3400.1.S1.W.A",
            {"type": "scene", "wlan": True, "scene": 1, "loads": 0},
        ],
        [
            # Bedienaufsatz Wiser Szenentaster 2 Szenen vertikal WLAN Gen.A
            "926-3400.2.VS.W.A",
            {"type": "scene", "wlan": True, "scene": 2, "loads": 0},
        ],
        [
            # Bedienaufsatz Wiser Szenentaster 4 Szenen WLAN Gen.A
            "926-3400.4.S4.W.A",
            {"type": "scene", "wlan": True, "scene": 4, "loads": 0},
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 1-Kanal WLAN Gen.A
            "926-3401.1.W.A",
            {"type": "switch", "wlan": True, "scene": 0, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 1-Kanal Szene WLAN Gen.A
            "926-3401.2.S1.W.A",
            {"type": "switch", "wlan": True, "scene": 1, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Druckschalter 2-Kanal WLAN Gen.A
            "926-3402.2.W.A",
            {"type": "switch", "wlan": True, "scene": 0, "loads": 2},
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 1-Kanal WLAN Gen.A
            "926-3404.2.W.A",
            {"type": "motor", "wlan": True, "scene": 0, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 1-Kanal Szene WLAN Gen.A
            "926-3404.4.S.W.A",
            {"type": "motor", "wlan": True, "scene": 1, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Storenschalter 2-Kanal WLAN Gen.A
            "926-3405.4.W.A",
            {"type": "motor", "wlan": True, "scene": 0, "loads": 2},
        ],
        [
            # Bedienaufsatz Wiser Dimmer 1-Kanal WLAN Gen.A
            "926-3406.2.W.A",
            {"type": "dimmer", "wlan": True, "scene": 0, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Dimmer 1-Kanal Szene WLAN Gen.A
            "926-3406.4.S.W.A",
            {"type": "dimmer", "wlan": True, "scene": 1, "loads": 1},
        ],
        [
            # Bedienaufsatz Wiser Dimmer 2-Kanal WLAN Gen.A
            "926-3407.4.W.A",
            {"type": "dimmer", "wlan": True, "scene": 0, "loads": 2},
        ],
    ]


def ref_a_data() -> list[list]:
    """Data provider for test_parse_wiser_device_ref_a"""
    return [
        ["3400.B.BSE", {"loads": 0, "type": "noop"}],
        ["3401.B.BSE", {"loads": 1, "type": "switch"}],
        ["3402.B.BSE", {"loads": 2, "type": "switch"}],
        ["3404.B.BSE", {"loads": 1, "type": "motor"}],
        ["3405.B.BSE", {"loads": 2, "type": "motor"}],
        ["3406.B.BSE", {"loads": 1, "type": "dimmer-led"}],
        ["3407.B.BSE", {"loads": 2, "type": "dimmer-led"}],
        ["3411.B.BSE", {"loads": 1, "type": "dimmer-dali"}],
    ]


@pytest.mark.parametrize("check_val", validate_str_data_valid())
def test_validate_str_valid(check_val: list):
    """Test validate_str with valid values"""
    valid = ["valid", "ok", "good"]
    validate_str(check_val, valid)
    assert True


def test_validate_str_invalid():
    """Test validate_str with invalid values"""

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
    """Test parse_wiser_device_ref_c"""
    actual = parse_wiser_device_ref_c(data[0])
    assert actual == data[1]


@pytest.mark.parametrize("data", ref_a_data())
def test_parse_wiser_device_ref_a(data: list):
    """Test parse_wiser_device_ref_a"""
    actual = parse_wiser_device_ref_a(data[0])
    assert actual == data[1]
