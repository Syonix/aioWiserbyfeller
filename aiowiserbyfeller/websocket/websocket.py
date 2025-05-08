"""Support for Websocket connections to µGateway."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
import json
import logging

import websockets.client

DEFAULT_WATCHDOG_TIMEOUT = 900
LOGGER = logging.getLogger(__name__)


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
        self._loop = asyncio.get_event_loop()
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

        self._timer_task = self._loop.call_later(
            self._timeout, lambda: asyncio.create_task(self.on_expire())
        )


class Websocket:
    """Wrapper for websocket connection to µGateway."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, host: str, token: str, logger: logging.Logger = LOGGER):
        """Initialize.

        Args:
            host: Hostname or IP of µGateway
            token: Secret token for connetion (see Auth.claim())
            logger: The logger to use.

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

    def subscribe(self, callback):
        """Add callback to be called when new data arrives."""
        self._subscribers.append(callback)

    def async_subscribe(self, callback):
        """Add async callback to be called when new data arrives."""
        self._async_subscribers.append(callback)

    def init(self):
        """Connect to µGateway."""
        asyncio.create_task(self.connect())  # noqa: RUF006

    async def connect(self):
        """Initiate connection and start message processing loop."""
        self._idle = False
        await self._watchdog.trigger()

        while True:
            try:
                async for ws in websockets.client.connect(
                    f"ws://{self._host}/api",
                    extra_headers={"Authorization": f"Bearer {self._token}"},
                ):
                    try:
                        async for message in ws:
                            await self.on_message(message)
                    except websockets.ConnectionClosed:
                        self._errcount += 1
                        if self._errcount > 10:
                            self._logger.error(
                                "µGateway websocket connection closed "
                                "10 times. Exiting connection..."
                            )
                            break

                        self._logger.warning(
                            "µGateway websocket connection closed. Reconnecting..."
                        )
                        continue
                    except (websockets.WebSocketException, ValueError) as e:
                        self.on_error(e)

                self._idle = True
                break

            except (websockets.WebSocketException, ValueError) as e:
                self.on_error(e)
                break

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

    async def on_watchdog_timeout(self):
        """Warn about watchdog timeout.

        Can be used as a default watchdog callback.
        """
        self._logger.warning(
            "Watchdog timeout. Doing nothing for now... Idle: %s", self._idle
        )
