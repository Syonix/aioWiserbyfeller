"""A collection of enums not related to a specific package."""

from enum import Enum


class BlinkPattern(Enum):
    """Available blink patterns."""

    RAMP = "ramp"
    RAMP_UP = "ramp_up"
    RAMP_DOWN = "ramp_down"
    PERMANENT = "permanent"
    SLOW = "slow"
    FAST = "fast"
