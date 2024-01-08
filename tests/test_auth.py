"""aiowiserbyfeller Auth class tests"""
import pytest
from aiowiserbyfeller.errors import (
    AuthorizationFailed,
    TokenMissing,
    UnsuccessfulRequest,
)
from .conftest import prepare_test, BASE_URL


@pytest.mark.asyncio
async def test_claim(client_auth, mock_aioresponse):
    """Test initial claiming request"""
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
async def test_request_token_missing(client_auth, mock_aioresponse):
    """Test if error handling works correctly."""
    response_json = {
        "message": "api is locked, log in to receive an authentication cookie OR unlock the device.",
        "status": "error",
    }
    mock_aioresponse.get(f"{BASE_URL}/time/now", payload=response_json)

    with pytest.raises(TokenMissing):
        await client_auth.request("get", f"time/now")


@pytest.mark.asyncio
async def test_request_unsuccessful(client_auth, mock_aioresponse):
    """Test if error handling works correctly."""
    response_json = {"message": "Specific error message", "status": "error"}
    mock_aioresponse.get(f"{BASE_URL}/time/now", payload=response_json)

    with pytest.raises(UnsuccessfulRequest, match="Specific error message"):
        await client_auth.request("get", f"time/now")
