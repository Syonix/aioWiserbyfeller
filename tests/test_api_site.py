"""aiowiserbyfeller Api class site tests."""

import pytest

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_site_info(client_api_auth, mock_aioresponse):
    """Test async_get_site_info."""
    response_json = {
        "status": "success",
        "data": {"rooms_order": [3, 7, 8, 2, 1], "scenes_order": [3, 4, 7]},
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/site", "get", response_json
    )

    actual = await client_api_auth.async_get_site_info()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_set_site_info(client_api_auth, mock_aioresponse):
    """Test async_set_site_info."""
    response_json = {
        "status": "success",
        "data": {"rooms_order": [3, 7, 8, 2, 1], "scenes_order": [3, 4, 7]},
    }

    request_json = {"rooms_order": [3, 7, 8, 2, 1], "scenes_order": [3, 4, 7]}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/site", "post", response_json, request_json
    )

    actual = await client_api_auth.async_set_site_info(request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_update_site_info(client_api_auth, mock_aioresponse):
    """Test async_update_site_info."""
    response_json = {
        "status": "success",
        "data": {
            "rooms_order": [3, 7, 8, 2, 1],
            "scenes_order": [3, 4, 7],
            "color": "yellow",
        },
    }

    request_json = {"color": "yellow"}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/site", "patch", response_json, request_json
    )

    actual = await client_api_auth.async_update_site_info(request_json)
    assert actual == response_json["data"]
