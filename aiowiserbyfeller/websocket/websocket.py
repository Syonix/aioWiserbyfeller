"""Support for Websocket connections to µGateway."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncGenerator, Awaitable, Callable
import json
import logging

import aiohttp
import websockets.client

DEFAULT_WATCHDOG_TIMEOUT = 900
LOGGER = logging.getLogger(__name__)


class _ConnectionClosed(Exception):
    """Signals that the WebSocket connection closed, triggering a reconnect attempt."""


class WebsocketWatchdog:
    """Watchdog to ensure websocket connection health."""

    def __init__(
        self,
        logger: logging.Logger,
        action: Callable[..., Awaitable],
        *,
        timeout_seconds: float = DEFAULT_WATCHDOG_TIMEOUT,
    ):
        """Initialize.

        Args:
            logger: The logger to use.
            action: The coroutine function to call when the watchdog expires.
            timeout_seconds: The number of seconds before the watchdog times out.

        """
        self._action = action
        self._logger = logger
        self._timeout = timeout_seconds
        self._timer_task: asyncio.TimerHandle | None = None

    def cancel(self) -> None:
        """Cancel the watchdog."""
        if self._timer_task:
            self._timer_task.cancel()
            self._timer_task = None

    async def on_expire(self) -> None:
        """Log and act when the watchdog expires."""
        self._logger.debug(
            "Watchdog expired - calling %s",
            getattr(self._action, "__name__", repr(self._action)),
        )
        await self._action()

    async def trigger(self) -> None:
        """Reset the watchdog timeout."""
        self._logger.debug(
            "Watchdog triggered - sleeping for %s seconds", self._timeout
        )

        if self._timer_task:
            self._timer_task.cancel()

        self._timer_task = asyncio.get_running_loop().call_later(
            self._timeout, lambda: asyncio.create_task(self.on_expire())
        )


class Websocket:
    """Wrapper for websocket connection to µGateway."""

    # pylint: disable=too-many-instance-attributes

    def __init__(
        self,
        host: str,
        token: str,
        logger: logging.Logger = LOGGER,
        *,
        session: aiohttp.ClientSession | None = None,
    ):
        """Initialize.

        Args:
            host: Hostname or IP of µGateway
            token: Secret token for connection (see Auth.claim())
            logger: The logger to use.
            session: Optional aiohttp ClientSession to use for the WebSocket
                connection. When provided, aiohttp's WebSocket client is used
                instead of the websockets library, which allows the caller
                (e.g. Home Assistant) to manage the session lifecycle, SSL
                certificates, and proxy settings centrally.

        """
        self._host = host
        self._token = token
        self._ws = None
        self._subscribers = []
        self._async_subscribers = []
        self._watchdog = WebsocketWatchdog(logger, self.on_watchdog_timeout)
        self._logger = logger
        self._errcount = 0
        self._idle = True
        self._session = session

    def subscribe(self, callback):
        """Add callback to be called when new data arrives."""
        self._subscribers.append(callback)

    def async_subscribe(self, callback):
        """Add async callback to be called when new data arrives."""
        self._async_subscribers.append(callback)

    def init(self):
        """Connect to µGateway."""
        asyncio.create_task(self.connect())  # noqa: RUF006

    async def connect(self) -> None:
        """Initiate connection and start message processing loop."""
        self._idle = False
        await self._watchdog.trigger()

        _iter = self._iter_aiohttp if self._session is not None else self._iter_websockets

        while True:
            try:
                async for message in _iter():
                    await self.on_message(message)
            except _ConnectionClosed:  # noqa: PERF203
                self._errcount += 1
                if self._errcount > 10:
                    self._logger.error(
                        "µGateway websocket connection closed "
                        "10 times. Exiting connection..."
                    )
                    self._idle = True
                    return
                self._logger.warning(
                    "µGateway websocket connection closed. Reconnecting..."
                )
                continue
            except Exception as e:  # noqa: BLE001
                self._idle = True
                self.on_error(e)
                return
            else:
                break

        self._idle = True

    async def _iter_websockets(self) -> AsyncGenerator[str, None]:
        """Yield messages from one websockets connection.

        Returns normally when the async-for ends without a ConnectionClosed
        exception (library converts ConnectionClosedOK to StopAsyncIteration).
        Raises _ConnectionClosed when a ConnectionClosed exception is received
        explicitly, so the outer loop reconnects. Other exceptions propagate
        as fatal errors.
        """
        async with websockets.client.connect(
            f"ws://{self._host}/api",
            extra_headers={"Authorization": f"Bearer {self._token}"},
        ) as ws:
            try:
                async for message in ws:
                    yield message
            except websockets.ConnectionClosed:
                raise _ConnectionClosed from None
            else:
                return

    async def _iter_aiohttp(self) -> AsyncGenerator[str, None]:
        """Yield messages from one aiohttp websocket connection.

        Raises _ConnectionClosed on CLOSE/CLOSING/CLOSED frames so the outer
        loop reconnects. ERROR frames and transport exceptions propagate as
        fatal errors.
        """
        async with self._session.ws_connect(  # type: ignore[union-attr]
            f"ws://{self._host}/api",
            headers={"Authorization": f"Bearer {self._token}"},
        ) as ws:
            self._ws = ws
            try:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        yield msg.data
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        exc = ws.exception()
                        raise exc if exc is not None else Exception("WebSocket error")
                    elif msg.type in (
                        aiohttp.WSMsgType.CLOSE,
                        aiohttp.WSMsgType.CLOSING,
                        aiohttp.WSMsgType.CLOSED,
                    ):
                        raise _ConnectionClosed
            finally:
                self._ws = None

    async def on_message(self, message):
        """Process new message."""
        data = json.loads(message)
        await self._watchdog.trigger()
        for fn in self._subscribers:
            fn(data)
        for fn in self._async_subscribers:
            await fn(data)

    def on_error(self, exception: Exception):
        """Process error."""
        self._logger.error("Websocket error: %s", exception)
        self._watchdog.cancel()
        raise exception

    def is_idle(self) -> bool:
        """Return True if the websocket connection is idle/disconnected."""
        return self._idle

    def reset_error_count(self) -> None:
        """Reset the connection error count to zero."""
        self._errcount = 0

    async def async_close(self) -> None:
        """Close the websocket connection if it exists."""
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:  # noqa: BLE001
                self._logger.debug("Error closing WebSocket connection, ignoring")
            self._ws = None
        self._watchdog.cancel()

    async def on_watchdog_timeout(self):
        """Warn about watchdog timeout.

        Can be used as a default watchdog callback.
        """
        self._logger.warning(
            "Watchdog timeout. Doing nothing for now... Idle: %s", self._idle
        )
