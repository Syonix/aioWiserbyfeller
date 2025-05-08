"""aiowiserbyfeller Auth class tests."""

import pytest

from aiowiserbyfeller.errors import (
    AuthorizationFailed,
    InvalidJson,
    TokenMissing,
    UnauthorizedUser,
    UnsuccessfulRequest,
)

from .conftest import BASE_URL, prepare_test  # noqa: TID251


@pytest.mark.asyncio
async def test_claim(client_auth, mock_aioresponse):
    """Test initial claiming request."""
    response_json = {
        "status": "success",
        "data": {
            "secret": "61b096f3-9f20-46db-932c-c8bbf7f6011d",
            "user": "enduser",
            "source": "installer",
        },
    }

    request_json = {"user": "enduser", "source": "installer"}

    await prepare_test(
        mock_aioresponse,
        f"{BASE_URL}/account/claim",
        "POST",
        response_json,
        request_json,
    )
    actual = await client_auth.claim("enduser")

    assert actual == response_json["data"]["secret"]


@pytest.mark.asyncio
async def test_claim_error(client_auth, mock_aioresponse):
    """Test if error handling works correctly."""
    response_json = {"status": "error", "message": "Precise error message here"}
    mock_aioresponse.post(f"{BASE_URL}/account/claim", payload=response_json)

    with pytest.raises(AuthorizationFailed, match="Precise error message here"):
        await client_auth.claim("installer")


@pytest.mark.asyncio
async def test_claim_invalid_json(client_auth, mock_aioresponse):
    """Test if handling of invalid JSON works correctly for claiming."""
    response_html = (
        '<!doctype html><html lang="en"><body><h1>Hello, world!</h1></body></html>'
    )
    mock_aioresponse.post(
        f"{BASE_URL}/account/claim", body=response_html, content_type="text/html"
    )

    with pytest.raises(InvalidJson):
        await client_auth.claim("installer")

    mock_aioresponse.post(f"{BASE_URL}/account/claim", body=response_html)

    with pytest.raises(InvalidJson):
        await client_auth.claim("installer")


@pytest.mark.asyncio
async def test_request_invalid_json(client_auth, mock_aioresponse):
    """Test if handling of invalid JSON works correctly for requests."""
    response_html = (
        '<!doctype html><html lang="en"><body><h1>Hello, world!</h1></body></html>'
    )
    mock_aioresponse.get(
        f"{BASE_URL}/info", body=response_html, content_type="text/html"
    )

    with pytest.raises(InvalidJson):
        await client_auth.request("get", "info", require_token=False)
    mock_aioresponse.get(f"{BASE_URL}/info", body=response_html)

    with pytest.raises(InvalidJson):
        await client_auth.request("get", "info", require_token=False)


@pytest.mark.asyncio
async def test_request_token_missing(client_auth, mock_aioresponse):
    """Test if error handling works correctly."""
    response_json = {
        "message": "api is locked, log in to receive an authentication cookie OR unlock the device.",
        "status": "error",
    }
    mock_aioresponse.get(f"{BASE_URL}/time/now", payload=response_json)

    with pytest.raises(TokenMissing):
        await client_auth.request("get", "time/now", require_token=False)

    with pytest.raises(TokenMissing):
        await client_auth.request("get", "some/path", require_token=True)


@pytest.mark.asyncio
async def test_request_unauthorized_user(client_auth, mock_aioresponse):
    """Test if error handling works correctly."""
    response_json = {
        "message": "unauthorized user",
        "status": "error",
    }
    mock_aioresponse.get(f"{BASE_URL}/time/now", payload=response_json)

    with pytest.raises(UnauthorizedUser):
        await client_auth.request("get", "time/now", require_token=False)


@pytest.mark.asyncio
async def test_request_unsuccessful(client_auth, mock_aioresponse):
    """Test if error handling works correctly."""
    response_json = {"message": "Specific error message", "status": "error"}
    mock_aioresponse.get(f"{BASE_URL}/time/now", payload=response_json)

    with pytest.raises(UnsuccessfulRequest, match="Specific error message"):
        await client_auth.request("get", "time/now", require_token=False)


@pytest.mark.asyncio
async def test_is_valid_login_success(client_auth, mock_aioresponse):
    """Test is_valid_login returns True if token is valid."""
    response_json = {"status": "success", "data": {"user": "installer"}}
    mock_aioresponse.get(f"{BASE_URL}/account", payload=response_json)

    client_auth.access_token = "token"
    result = await client_auth.is_valid_login()

    assert result is True


@pytest.mark.asyncio
async def test_is_valid_login_failure(client_auth, mock_aioresponse):
    """Test is_valid_login returns False if token is not valid."""
    response_json = {"status": "error", "message": "some error"}
    mock_aioresponse.get(f"{BASE_URL}/account", payload=response_json)

    client_auth.access_token = "token"
    result = await client_auth.is_valid_login()

    assert result is False


@pytest.mark.asyncio
async def test_request_merges_headers(client_auth, mock_aioresponse):
    """Test that custom headers are merged and token is added."""
    client_auth.access_token = "abc123"

    response_json = {"status": "success", "data": {"value": 42}}
    mock_aioresponse.get(f"{BASE_URL}/some/path", payload=response_json)

    result = await client_auth.request("get", "some/path", headers={"X-Test": "value"})

    assert result == {"value": 42}
