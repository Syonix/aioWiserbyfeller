"""aiowiserbyfeller Api class scripts tests."""

import pytest

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_scripts(client_api_auth, mock_aioresponse):
    """Test async_get_scripts."""
    response_json = {
        "status": "success",
        "data": [
            {"name": "hello_world.py", "size": 740},
            {"name": "test.py", "size": 120},
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/scripts", "get", response_json
    )

    actual = await client_api_auth.async_get_scripts()

    assert len(actual) == 2
    assert actual[0]["name"] == "hello_world.py"
    assert actual[0]["size"] == 740


@pytest.mark.asyncio
async def test_async_upload_script(client_api_auth, mock_aioresponse):
    """Test async_upload_script."""
    response_json = {
        "status": "success",
        "data": {"name": "hello_world.py", "size": 740},
    }

    # Binary upload — we don't verify request body via prepare_test_authenticated
    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/scripts/hello_world.py",
        "post",
        response_json,
    )

    actual = await client_api_auth.async_upload_script(
        "hello_world.py", b"print('hello world')"
    )

    assert actual["name"] == "hello_world.py"
    assert actual["size"] == 740


@pytest.mark.asyncio
async def test_async_delete_script(client_api_auth, mock_aioresponse):
    """Test async_delete_script."""
    response_json = {
        "status": "success",
        "data": {"name": "hello_world.py", "size": 740},
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/scripts/hello_world.py",
        "delete",
        response_json,
    )

    actual = await client_api_auth.async_delete_script("hello_world.py")

    assert actual["name"] == "hello_world.py"


@pytest.mark.asyncio
async def test_async_start_script(client_api_auth, mock_aioresponse):
    """Test async_start_script."""
    response_json = {"status": "success", "data": None}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/scripts/hello_world.py/start",
        "get",
        response_json,
    )

    await client_api_auth.async_start_script("hello_world.py")


@pytest.mark.asyncio
async def test_async_stop_script(client_api_auth, mock_aioresponse):
    """Test async_stop_script."""
    response_json = {"status": "success", "data": None}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/scripts/hello_world.py/stop",
        "get",
        response_json,
    )

    await client_api_auth.async_stop_script("hello_world.py")


@pytest.mark.asyncio
async def test_async_get_scripts_cron(client_api_auth, mock_aioresponse):
    """Test async_get_scripts_cron."""
    cron_entries = [
        "* * * * * /scripts.test1_script.onCronEvent",
        "*/3 * * * * /scripts.test2_script.onCronEvent",
    ]
    response_json = {"status": "success", "data": cron_entries}

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/scripts/cron", "get", response_json
    )

    actual = await client_api_auth.async_get_scripts_cron()

    assert len(actual) == 2
    assert actual[0] == "* * * * * /scripts.test1_script.onCronEvent"


@pytest.mark.asyncio
async def test_async_set_script_cron(client_api_auth, mock_aioresponse):
    """Test async_set_script_cron."""
    request_json = {"entry": "* * * * *"}
    response_json = {
        "status": "success",
        "data": {"cron_job": "* * * * * /scripts.hello_world.onCronEvent"},
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/scripts/hello_world.py/cron",
        "patch",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_set_script_cron("hello_world.py", "* * * * *")

    assert actual["cron_job"] == "* * * * * /scripts.hello_world.onCronEvent"


@pytest.mark.asyncio
async def test_async_delete_script_cron(client_api_auth, mock_aioresponse):
    """Test async_delete_script_cron."""
    response_json = {
        "status": "success",
        "data": {"cron_job": "* * * * * /scripts.hello_world.onCronEvent"},
    }

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/scripts/hello_world.py/cron",
        "delete",
        response_json,
    )

    actual = await client_api_auth.async_delete_script_cron("hello_world.py")

    assert actual["cron_job"] == "* * * * * /scripts.hello_world.onCronEvent"
