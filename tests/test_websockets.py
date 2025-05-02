"""aiowiserbyfeller websocket tests"""

import asyncio
import pytest
import logging
from unittest.mock import AsyncMock, Mock, patch

from aiowiserbyfeller import Websocket, WebsocketWatchdog


def get_test_logger():
    logger = logging.getLogger("test_logger")
    logger.addHandler(logging.NullHandler())

    return logger


@pytest.mark.asyncio
async def test_watchdog_triggers_action():
    action = AsyncMock()
    watchdog = WebsocketWatchdog(
        logger=get_test_logger(), action=action, timeout_seconds=0.1
    )

    await watchdog.trigger()
    await asyncio.sleep(0.2)  # wait for the watchdog to expire

    action.assert_called_once()


@pytest.mark.asyncio
async def test_watchdog_cancel_prevents_expiration():
    called = []

    async def dummy_action():
        called.append("expired")

    watchdog = WebsocketWatchdog(
        logger=get_test_logger(), action=dummy_action, timeout_seconds=0.1
    )
    await watchdog.trigger()
    watchdog.cancel()

    await asyncio.sleep(0.2)  # ensure enough time passes
    assert not called  # Action should not have been called


@pytest.mark.asyncio
async def test_on_message_triggers_subscribers():
    ws = Websocket("host", "token")

    sync_cb = Mock()
    async_cb = AsyncMock()

    ws.subscribe(sync_cb)
    ws.async_subscribe(async_cb)

    test_message = '{"status": "ok"}'
    await ws.on_message(test_message)

    sync_cb.assert_called_once_with({"status": "ok"})
    async_cb.assert_awaited_once_with({"status": "ok"})


def test_on_error_cancels_watchdog():
    ws = Websocket("host", "token")
    ws._watchdog = Mock()

    with pytest.raises(Exception):
        ws.on_error(Exception("fail"))

    ws._watchdog.cancel.assert_called_once()


@patch("aiowiserbyfeller.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_connect_receives_message(mock_connect):
    # Simulate a single websocket yielding a single message
    mock_ws = AsyncMock()
    mock_ws.__aiter__.return_value = iter(['{"status": "ok"}'])
    mock_connect.return_value.__aiter__.return_value = iter([mock_ws])

    ws = Websocket("host", "token")
    sync_cb = Mock()
    ws.subscribe(sync_cb)

    # Patch watchdog to prevent timeout complications
    ws._watchdog = AsyncMock()

    await ws.connect()

    sync_cb.assert_called_once_with({"status": "ok"})
    mock_connect.assert_called_once()
