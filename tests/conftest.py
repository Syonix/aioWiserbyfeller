"""Prepare for unit tests."""

import inspect
import logging
from unittest.mock import Mock

import aiohttp
from aioresponses import aioresponses
import pytest
import pytest_asyncio

# aiohttp 3.14 added stream_writer as a required argument to ClientResponse.__init__,
# but aioresponses 0.7.8 doesn't pass it yet (https://github.com/pnuckowski/aioresponses/pull/288).
if "stream_writer" in inspect.signature(aiohttp.ClientResponse).parameters:
    _orig_client_response_init = aiohttp.ClientResponse.__init__

    def _client_response_init_compat(self, *args, stream_writer=None, **kwargs):
        if stream_writer is None:
            stream_writer = Mock(output_size=0)
        _orig_client_response_init(self, *args, stream_writer=stream_writer, **kwargs)

    aiohttp.ClientResponse.__init__ = _client_response_init_compat

from aiowiserbyfeller import Auth, WiserByFellerAPI

BASE_URL = "http://192.168.0.1/api"
BASE_DATA_PATH = "tests/data/devices"
TEST_API_TOKEN = "TEST-API-TOKEN"


@pytest.fixture
def test_logger():
    """Create a test logger."""
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.NullHandler())

    return logger


@pytest.fixture
def mock_aioresponse():
    """Prepare mocks."""
    with aioresponses() as m:
        yield m


@pytest_asyncio.fixture(scope="function")
async def client_auth():
    """Initialize Auth instance."""
    async with aiohttp.ClientSession() as http:
        result = Auth(http, "192.168.0.1")
        yield result


@pytest_asyncio.fixture(scope="function")
async def client_api(client_auth):
    """Initialize Api instance."""
    result = WiserByFellerAPI(client_auth)
    yield result


@pytest_asyncio.fixture(scope="function")
async def client_api_auth():
    """Initialize authenticated Api instance."""
    async with aiohttp.ClientSession() as http:
        auth = Auth(http, "192.168.0.1", token=TEST_API_TOKEN)
        result = WiserByFellerAPI(auth)
        yield result


async def prepare_test(mock, url, method, response, request=None):
    """Return a mock callback for an unauthenticated test case."""

    def mock_callback(callback_url, **kwargs):
        assert kwargs.get("json") == request

    mock.add(url, method, payload=response, callback=mock_callback)


async def prepare_test_authenticated(mock, url, method, response, request=None):
    """Return a mock callback for an authenticated test case."""

    def mock_callback(callback_url, **kwargs):
        assert kwargs.get("json") == request
        auth_header = kwargs.get("headers")["authorization"]
        assert auth_header == f"Bearer: {TEST_API_TOKEN}"

    mock.add(url, method, payload=response, callback=mock_callback)
