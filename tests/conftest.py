"""Prepare for unit tests"""
import pytest
import aiohttp
from aioresponses import aioresponses
from aiowiserbyfeller import Auth, WiserByFellerAPI

BASE_URL = "http://192.168.0.1/api"
TEST_API_TOKEN = "TEST-API-TOKEN"


@pytest.fixture
def mock_aioresponse():
    """Prepare mocks"""
    with aioresponses() as m:
        yield m


@pytest.fixture(scope="module")
def client_auth():
    """Initialize Auth instance"""
    http = aiohttp.ClientSession()
    result = Auth(http, "192.168.0.1")
    yield result


@pytest.fixture(scope="module")
def client_api(client_auth):
    """Initialize Api instance"""
    result = WiserByFellerAPI(client_auth)
    yield result


@pytest.fixture(scope="module")
def client_api_auth():
    """Initialize authenticated Api instance"""
    http = aiohttp.ClientSession()
    auth = Auth(http, "192.168.0.1", token=TEST_API_TOKEN)
    result = WiserByFellerAPI(auth)
    yield result


async def prepare_test(mock, url, method, response, request=None):
    def mock_callback(url, **kwargs):
        assert kwargs.get("json") == request

    mock.add(url, method, payload=response, callback=mock_callback)


async def prepare_test_authenticated(mock, url, method, response, request=None):
    def mock_callback(url, **kwargs):
        assert kwargs.get("json") == request
        auth_header = kwargs.get("headers")["authorization"]
        assert auth_header == f"Bearer: {TEST_API_TOKEN}"

    mock.add(url, method, payload=response, callback=mock_callback)
