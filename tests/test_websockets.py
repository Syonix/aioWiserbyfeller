"""aiowiserbyfeller websocket tests"""

import asyncio
import pytest
from unittest.mock import AsyncMock, Mock, patch

from aiowiserbyfeller import Websocket, WebsocketWatchdog


@pytest.mark.asyncio
async def test_watchdog_triggers_action(test_logger):
    action = AsyncMock()
    watchdog = WebsocketWatchdog(logger=test_logger, action=action, timeout_seconds=0.1)

    await watchdog.trigger()
    await asyncio.sleep(0.2)  # wait for the watchdog to expire

    action.assert_called_once()


@pytest.mark.asyncio
async def test_watchdog_cancel_prevents_expiration(test_logger):
    called = []

    async def dummy_action():
        called.append("expired")

    watchdog = WebsocketWatchdog(
        logger=test_logger, action=dummy_action, timeout_seconds=0.1
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


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
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


@pytest.mark.asyncio
async def test_watchdog_trigger_cancels_previous(test_logger):
    action = AsyncMock()
    watchdog = WebsocketWatchdog(logger=test_logger, action=action, timeout_seconds=0.5)

    await watchdog.trigger()
    first_timer = watchdog._timer_task

    await asyncio.sleep(0.1)
    await watchdog.trigger()  # This should cancel the first timer
    second_timer = watchdog._timer_task

    assert first_timer.cancelled(), "First timer should be cancelled"
    assert second_timer is not None
    assert first_timer is not second_timer


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_connect_handles_connection_closed(mock_connect, test_logger):
    from websockets.frames import Close
    from websockets.exceptions import ConnectionClosedOK

    mock_ws = AsyncMock()
    mock_ws.__aiter__.side_effect = ConnectionClosedOK(Close(1000, "closed"), None)
    mock_connect.return_value.__aiter__.return_value = iter([mock_ws])

    ws = Websocket("host", "token", logger=test_logger)
    ws._watchdog = AsyncMock()

    with patch.object(ws, "_logger") as mock_logger:
        await ws.connect()
        assert mock_logger.warning.called


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_connect_handles_websocket_exception(mock_connect, test_logger):
    from websockets.exceptions import WebSocketException

    # Simulate connect() itself raising the exception
    mock_connect.side_effect = WebSocketException("fail")

    ws = Websocket("host", "token", logger=test_logger)
    ws._watchdog = AsyncMock()

    with patch.object(ws, "on_error") as mock_on_error:
        await ws.connect()
        mock_on_error.assert_called_once()


@pytest.mark.asyncio
async def test_on_watchdog_timeout_logs(test_logger):
    ws = Websocket("host", "token", logger=test_logger)
    ws._idle = True

    with patch.object(ws._logger, "warning") as mock_warn:
        await ws.on_watchdog_timeout()
        mock_warn.assert_called_once()
        assert "Watchdog timeout" in mock_warn.call_args[0][0]


@patch("aiowiserbyfeller.websocket.websocket.asyncio.create_task")
def test_websocket_init_starts_connection(mock_create_task, test_logger):
    ws = Websocket("host", "token", logger=test_logger)
    ws.init()
    mock_create_task.assert_called_once()


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_websocket_stops_after_10_failures(mock_connect, test_logger):
    from websockets.frames import Close
    from websockets.exceptions import ConnectionClosed

    # Create a mock websocket that simulates 11 reconnects, each with a message
    class FakeWebSocket:
        def __init__(self):
            self._messages = ['{"status": "ok"}']  # valid JSON string

        def __aiter__(self):
            return self

        async def __anext__(self):
            raise ConnectionClosed(Close(1000, "closed"), None)

    # Simulate 11 websocket instances (each closes immediately)
    mock_connect.return_value.__aiter__.return_value = [FakeWebSocket()] * 11

    ws = Websocket("host", "token", logger=test_logger)
    ws._watchdog = AsyncMock()

    with patch.object(ws._logger, "error") as mock_log_error:
        await ws.connect()
        mock_log_error.assert_called_once()
        assert ws._errcount == 11


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_websocket_exception_triggers_on_error(mock_connect, test_logger):
    from websockets.exceptions import WebSocketException

    class FailingAsyncIterable:
        def __aiter__(self):
            return self

        async def __anext__(self):
            raise WebSocketException("oops")

    mock_connect.return_value = FailingAsyncIterable()

    ws = Websocket("host", "token", logger=test_logger)
    ws._watchdog = AsyncMock()

    with patch.object(ws, "on_error", return_value=None) as mock_on_error:
        await ws.connect()
        mock_on_error.assert_called_once()
