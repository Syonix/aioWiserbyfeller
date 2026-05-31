"""Tests for Wiser button LED API."""

from unittest.mock import AsyncMock

import pytest

from aiowiserbyfeller import Button
from aiowiserbyfeller.enum import BlinkPattern


@pytest.mark.asyncio
async def test_set_button_led(client_api):
    """Test api.async_set_button_led delegates to Button.async_set_led."""
    client_api.auth.request = AsyncMock(return_value={})

    await client_api.async_set_button_led(
        button_id=12,
        led_index=1,
        on=True,
        pattern=BlinkPattern.FAST,
        color="#00FF00",
    )

    client_api.auth.request.assert_awaited_once_with(
        "put",
        "buttons/12/leds/1",
        json={
            "on": True,
            "pattern": "fast",
            "color": "#00FF00",
        },
    )


@pytest.mark.asyncio
async def test_button_async_set_led(client_api):
    """Test Button.async_set_led."""
    client_api.auth.request = AsyncMock(return_value={})

    button = Button({"id": 12}, client_api.auth)
    await button.async_set_led(
        led_index=1,
        on=True,
        pattern=BlinkPattern.FAST,
        color="#00FF00",
    )

    client_api.auth.request.assert_awaited_once_with(
        "put",
        "buttons/12/leds/1",
        json={
            "on": True,
            "pattern": "fast",
            "color": "#00FF00",
        },
    )
