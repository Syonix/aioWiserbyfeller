"""aiowiserbyfeller websocket tests."""

import asyncio
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, Mock, patch

import aiohttp
import pytest
from websockets.exceptions import (
    ConnectionClosed,
    ConnectionClosedOK,
    WebSocketException,
)
from websockets.frames import Close

from aiowiserbyfeller import Websocket, WebsocketWatchdog


def make_ws_message(msg_type, data=None):
    """Create an aiohttp WSMessage."""
    return aiohttp.WSMessage(msg_type, data, None)


def make_mock_session(*message_sequences):
    """Build a mock aiohttp ClientSession whose ws_connect yields message sequences.

    Each positional argument is a list of WSMessage objects representing one
    connection lifetime. The mock reconnects for each sequence in order.
    aiohttp's ws_connect() is a sync call returning an async context manager,
    so fake_ws_connect must be a regular function, not a coroutine.
    """
    call_count = 0

    mock_session = Mock()

    def fake_ws_connect(url, headers=None):
        nonlocal call_count
        messages = (
            message_sequences[call_count] if call_count < len(message_sequences) else []
        )
        call_count += 1

        mock_ws = AsyncMock()
        mock_ws.exception.return_value = None

        async def aiter_messages():
            for msg in messages:
                yield msg

        mock_ws.__aiter__ = lambda self: aiter_messages()

        @asynccontextmanager
        async def ctx():
            yield mock_ws

        return ctx()

    mock_session.ws_connect = fake_ws_connect
    return mock_session


def make_mock_ws_connect(*connection_specs):
    """Return a callable for websockets.client.connect (use as mock side_effect).

    Each positional argument is either:
    - list[str]: messages to yield, then return normally (no reconnect)
    - tuple[list[str], Exception]: messages to yield, then raise the exception

    Calls beyond the number of specs return an empty connection (clean exit).
    """
    call_count = 0

    def fake_connect(uri, **kwargs):
        nonlocal call_count
        spec = connection_specs[call_count] if call_count < len(connection_specs) else []
        call_count += 1

        messages, close_exc = (spec, None) if isinstance(spec, list) else spec

        mock_ws = AsyncMock()

        async def aiter_messages():
            for msg in messages:
                yield msg
            if close_exc is not None:
                raise close_exc

        mock_ws.__aiter__ = lambda self: aiter_messages()

        @asynccontextmanager
        async def ctx():
            yield mock_ws

        return ctx()

    return fake_connect


@pytest.mark.asyncio
async def test_watchdog_triggers_action(test_logger):
    """Test that the watchdog triggers after a timeout."""
    action = AsyncMock()
    watchdog = WebsocketWatchdog(logger=test_logger, action=action, timeout_seconds=0.1)

    await watchdog.trigger()
    await asyncio.sleep(0.2)  # wait for the watchdog to expire

    action.assert_called_once()


@pytest.mark.asyncio
async def test_watchdog_cancel_prevents_expiration(test_logger):
    """Test that cancelling the watchdog works."""
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
    """Test that a message triggers subscribers."""
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
    """Test that an error cancels the watchdog."""
    ws = Websocket("host", "token")
    ws._watchdog = Mock()  # noqa: SLF001

    with pytest.raises(Exception):  # noqa: B017
        ws.on_error(Exception("fail"))

    ws._watchdog.cancel.assert_called_once()  # noqa: SLF001


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_connect_receives_message(mock_connect):
    """Test connecting."""
    mock_connect.side_effect = make_mock_ws_connect(['{"status": "ok"}'])

    ws = Websocket("host", "token")
    sync_cb = Mock()
    ws.subscribe(sync_cb)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    await ws.connect()

    sync_cb.assert_called_once_with({"status": "ok"})
    mock_connect.assert_called_once()


@pytest.mark.asyncio
async def test_watchdog_trigger_cancels_previous(test_logger):
    """Test that watchdog cancels previous timeouts when triggered."""
    action = AsyncMock()
    watchdog = WebsocketWatchdog(logger=test_logger, action=action, timeout_seconds=0.5)

    await watchdog.trigger()
    first_timer = watchdog._timer_task  # noqa: SLF001

    await asyncio.sleep(0.1)
    await watchdog.trigger()  # This should cancel the first timer
    second_timer = watchdog._timer_task  # noqa: SLF001

    assert first_timer.cancelled(), "First timer should be cancelled"
    assert second_timer is not None
    assert first_timer is not second_timer


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_connect_handles_connection_closed(mock_connect, test_logger):
    """Test that connect method handles closed connections."""
    mock_connect.side_effect = make_mock_ws_connect(
        ([], ConnectionClosedOK(Close(1000, "closed"), None)),  # first: raises OK
        [],  # second: empty, clean exit
    )

    ws = Websocket("host", "token", logger=test_logger)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    with patch.object(ws, "_logger") as mock_logger:
        await ws.connect()
        assert mock_logger.warning.called


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_connect_handles_websocket_exception(mock_connect, test_logger):
    """Test that websocket exceptions are handled in connect method."""

    # Simulate connect() itself raising the exception
    mock_connect.side_effect = WebSocketException("fail")

    ws = Websocket("host", "token", logger=test_logger)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    with patch.object(ws, "on_error") as mock_on_error:
        await ws.connect()
        mock_on_error.assert_called_once()


@pytest.mark.asyncio
async def test_on_watchdog_timeout_logs(test_logger):
    """Test that watchdog timeouts are logged."""
    ws = Websocket("host", "token", logger=test_logger)
    ws._idle = True  # noqa: SLF001

    with patch.object(ws._logger, "warning") as mock_warn:  # noqa: SLF001
        await ws.on_watchdog_timeout()
        mock_warn.assert_called_once()
        assert "Watchdog timeout" in mock_warn.call_args[0][0]


def test_is_idle_returns_idle_state():
    """Test that is_idle() reflects the internal idle state."""
    ws = Websocket("host", "token")
    assert ws.is_idle() is True
    ws._idle = False  # noqa: SLF001
    assert ws.is_idle() is False


def test_reset_error_count_resets_to_zero():
    """Test that reset_error_count() resets _errcount to zero."""
    ws = Websocket("host", "token")
    ws._errcount = 7  # noqa: SLF001
    ws.reset_error_count()
    assert ws._errcount == 0  # noqa: SLF001


@pytest.mark.asyncio
async def test_async_close_closes_and_clears_ws():
    """Test that async_close() closes the connection and cancels the watchdog."""
    ws = Websocket("host", "token")
    mock_ws_conn = AsyncMock()
    ws._ws = mock_ws_conn  # noqa: SLF001
    ws._watchdog = Mock()  # noqa: SLF001

    await ws.async_close()

    mock_ws_conn.close.assert_awaited_once()
    assert ws._ws is None  # noqa: SLF001
    ws._watchdog.cancel.assert_called_once()  # noqa: SLF001


@pytest.mark.asyncio
async def test_async_close_when_already_closed():
    """Test that async_close() is safe to call when no connection exists."""
    ws = Websocket("host", "token")
    ws._watchdog = Mock()  # noqa: SLF001

    await ws.async_close()  # _ws is None — should not raise

    ws._watchdog.cancel.assert_called_once()  # noqa: SLF001


@pytest.mark.asyncio
async def test_async_close_swallows_close_exception():
    """Test that async_close() ignores exceptions raised by ws.close()."""
    ws = Websocket("host", "token")
    mock_ws_conn = AsyncMock()
    mock_ws_conn.close.side_effect = Exception("boom")
    ws._ws = mock_ws_conn  # noqa: SLF001
    ws._watchdog = Mock()  # noqa: SLF001

    await ws.async_close()  # should not raise

    assert ws._ws is None  # noqa: SLF001
    ws._watchdog.cancel.assert_called_once()  # noqa: SLF001


@patch("aiowiserbyfeller.websocket.websocket.asyncio.create_task")
def test_websocket_init_starts_connection(mock_create_task, test_logger):
    """Test that init() does start a connection."""
    ws = Websocket("host", "token", logger=test_logger)
    ws.init()
    mock_create_task.assert_called_once()


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_websocket_stops_after_10_failures(mock_connect, test_logger):
    """Test that websocket stops after 11 consecutive connection-closed events."""
    close_exc = ConnectionClosed(Close(1000, "closed"), None)
    mock_connect.side_effect = make_mock_ws_connect(*[([], close_exc)] * 11)

    ws = Websocket("host", "token", logger=test_logger)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    with patch.object(ws._logger, "error") as mock_log_error:  # noqa: SLF001
        await ws.connect()
        mock_log_error.assert_called_once()
        assert ws._errcount == 11  # noqa: SLF001


@patch("aiowiserbyfeller.websocket.websocket.websockets.client.connect")
@pytest.mark.asyncio
async def test_websocket_exception_triggers_on_error(mock_connect, test_logger):
    """Test that a non-ConnectionClosed websocket exception triggers on_error."""
    mock_connect.side_effect = make_mock_ws_connect(
        ([], WebSocketException("oops"))
    )

    ws = Websocket("host", "token", logger=test_logger)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    with patch.object(ws, "on_error", return_value=None) as mock_on_error:
        await ws.connect()
        mock_on_error.assert_called_once()


# ---------------------------------------------------------------------------
# aiohttp session injection tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_aiohttp_connect_receives_text_message(test_logger):
    """Injected session: TEXT messages are dispatched to subscribers."""
    messages = [make_ws_message(aiohttp.WSMsgType.TEXT, '{"status": "ok"}')]
    session = make_mock_session(messages)

    ws = Websocket("host", "token", logger=test_logger, session=session)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    sync_cb = Mock()
    ws.subscribe(sync_cb)

    await ws.connect()

    sync_cb.assert_called_once_with({"status": "ok"})


@pytest.mark.asyncio
async def test_aiohttp_connect_reconnects_on_close(test_logger):
    """Injected session: CLOSE message triggers a reconnect (second connection processes a message)."""
    first = [make_ws_message(aiohttp.WSMsgType.CLOSE)]
    second = [make_ws_message(aiohttp.WSMsgType.TEXT, '{"status": "ok"}')]
    session = make_mock_session(first, second)

    ws = Websocket("host", "token", logger=test_logger, session=session)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    sync_cb = Mock()
    ws.subscribe(sync_cb)

    await ws.connect()

    sync_cb.assert_called_once_with({"status": "ok"})
    assert ws._errcount == 1  # noqa: SLF001


@pytest.mark.asyncio
async def test_aiohttp_connect_stops_after_10_failures(test_logger):
    """Injected session: stops and logs an error after 11 consecutive CLOSE messages."""
    close_sequences = [[make_ws_message(aiohttp.WSMsgType.CLOSE)]] * 11
    session = make_mock_session(*close_sequences)

    ws = Websocket("host", "token", logger=test_logger, session=session)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    with patch.object(ws._logger, "error") as mock_log_error:  # noqa: SLF001
        await ws.connect()
        mock_log_error.assert_called_once()
        assert ws._errcount == 11  # noqa: SLF001
        assert ws.is_idle()


@pytest.mark.asyncio
async def test_aiohttp_connect_handles_client_error(test_logger):
    """Injected session: aiohttp.ClientError triggers on_error."""
    mock_session = Mock()
    mock_session.ws_connect = Mock(
        side_effect=aiohttp.ClientError("connection refused")
    )

    ws = Websocket("host", "token", logger=test_logger, session=mock_session)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    with patch.object(ws, "on_error", return_value=None) as mock_on_error:
        await ws.connect()
        mock_on_error.assert_called_once()


@pytest.mark.asyncio
async def test_aiohttp_connect_handles_error_message(test_logger):
    """Injected session: WSMsgType.ERROR triggers on_error with the ws exception."""
    exc = Exception("ws protocol error")
    messages = [make_ws_message(aiohttp.WSMsgType.ERROR)]
    session = make_mock_session(messages)

    ws = Websocket("host", "token", logger=test_logger, session=session)
    ws._watchdog = AsyncMock()  # noqa: SLF001

    # Patch the mock ws to return our exception
    def patched_ws_connect(url, headers=None):
        mock_ws = AsyncMock()
        mock_ws.exception = Mock(return_value=exc)

        async def aiter_messages():
            yield make_ws_message(aiohttp.WSMsgType.ERROR)

        mock_ws.__aiter__ = lambda self: aiter_messages()

        @asynccontextmanager
        async def ctx():
            yield mock_ws

        return ctx()

    session.ws_connect = patched_ws_connect

    with patch.object(ws, "on_error", return_value=None) as mock_on_error:
        await ws.connect()
        mock_on_error.assert_called_once_with(exc)


def test_websocket_with_session_uses_aiohttp_path():
    """Passing session= stores it and routes connect() to the aiohttp path."""
    mock_session = Mock(spec=aiohttp.ClientSession)
    ws = Websocket("host", "token", session=mock_session)
    assert ws._session is mock_session  # noqa: SLF001


def test_websocket_without_session_uses_websockets_path():
    """Default (no session) keeps _session as None for the websockets path."""
    ws = Websocket("host", "token")
    assert ws._session is None  # noqa: SLF001
