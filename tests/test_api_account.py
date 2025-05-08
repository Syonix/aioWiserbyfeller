"""aiowiserbyfeller Api class account tests."""

import pytest

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_clone_account(client_api_auth, mock_aioresponse):
    """Test async_clone_account."""
    response_json = {
        "status": "success",
        "data": {
            "secret": "20e55c5e-3893-40de-a3fa-00fe7c26d2fe",
            "source": "admin",
            "user": "felix",
            "login": "fkunz",
            "company": "Foobar Electrical Building Tech. Ltd.",
            "name": "Felix Kunz",
        },
    }

    request_json = {
        "user": "installer",
        "login": "fkunz",
        "company": "Foobar Electrical Building Tech. Ltd.",
        "name": "Felix Kunz",
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/account/clone",
        "post",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_clone_account(
        "installer",
        login="fkunz",
        company="Foobar Electrical Building Tech. Ltd.",
        name="Felix Kunz",
    )
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_clones(client_api_auth, mock_aioresponse):
    """Test async_get_clones."""
    response_json = {
        "status": "success",
        "data": [{"user": "admin", "secret": "5b9b2996-04bd-4762-9c4a-f9b043c34deb"}],
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/account/clones",
        "get",
        response_json,
    )

    actual = await client_api_auth.async_get_clones()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_get_account(client_api_auth, mock_aioresponse):
    """Test async_get_account."""
    response_json = {
        "status": "success",
        "data": {
            "user": "admin",
            "source": "installer",
            "login": "mmeier",
            "company": "Foobar Electrical Building Tech. Ltd.",
            "name": "Martin Meier",
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/account",
        "get",
        response_json,
    )

    actual = await client_api_auth.async_get_account()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_update_account(client_api_auth, mock_aioresponse):
    """Test async_update_account."""
    response_json = {
        "status": "success",
        "data": {
            "user": "admin",
            "source": "installer",
            "login": "mmeier",
            "company": "Foobar Electrical Building Tech. Ltd.",
            "name": "Martin Meier",
            "eye-color": "green",
        },
    }

    request_json = {"eye-color": "green"}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/account", "patch", response_json, request_json
    )

    actual = await client_api_auth.async_update_account(request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_delete_account(client_api_auth, mock_aioresponse):
    """Test async_delete_account."""
    response_json = {
        "status": "success",
        "data": {
            "user": "admin",
            "source": "installer",
            "login": "mmeier",
            "company": "Foobar Electrical Building Tech. Ltd.",
            "name": "Martin Meier",
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/account", "delete", response_json
    )

    actual = await client_api_auth.async_delete_account()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_reset_account(client_api_auth, mock_aioresponse):
    """Test async_reset_account."""
    response_json = {
        "status": "success",
        "data": {
            "user": "admin",
            "source": "installer",
            "login": "mmeier",
            "company": "Foobar Electrical Building Tech. Ltd.",
            "name": "Martin Meier",
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/account/reset", "post", response_json
    )

    actual = await client_api_auth.async_reset_account()
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_sync_account(client_api_auth, mock_aioresponse):
    """Test async_sync_account."""
    response_json = {"status": "success", "data": None}
    request_json = {
        "secrets": ["5b9b2996-04bd-4762-9c4a-f9b043c34deb"],
        "sync": {"rooms": [10, 11], "scenes": [20, 21]},
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/account/sync",
        "post",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_sync_account(request_json)
    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_async_sync_account_clones(client_api_auth, mock_aioresponse):
    """Test async_sync_account_clones."""
    response_json = {"status": "success", "data": None}
    request_json = {"sync": {"rooms": [10, 11], "scenes": [20, 21]}}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/account/clones/sync",
        "post",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_sync_account_clones(request_json)
    assert actual == response_json["data"]
