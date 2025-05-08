"""aiowiserbyfeller Api class jobs tests."""

import pytest

from aiowiserbyfeller import InvalidArgument, Job

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_jobs(client_api_auth, mock_aioresponse):
    """Test async_get_jobs."""
    response_json = {
        "status": "success",
        "data": [
            {
                "id": 7,
                "target_states": [{"load": 9, "bri": 7500}],
                "flag_values": [{"flag": 39, "value": True}],
                "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
                "scripts": ["test.py"],
                "blocked_by": 10,
                "triggers": [5],
            }
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/jobs", "get", response_json
    )

    actual = await client_api_auth.async_get_jobs()

    assert len(actual) == 1
    assert isinstance(actual[0], Job)
    assert actual[0].id == 7
    assert actual[0].target_states[0]["bri"] == 7500


@pytest.mark.asyncio
async def test_async_create_job(client_api_auth, mock_aioresponse):
    """Test async_create_job."""
    response_json = {
        "status": "success",
        "data": {
            "id": 7,
            "target_states": [{"load": 9, "bri": 7500}],
            "flag_values": [{"flag": 39, "value": True}],
            "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
            "scripts": ["test.py"],
            "blocked_by": 10,
            "triggers": [5],
        },
    }

    request_json = {
        "flag_values": [{"flag": 39, "value": True}],
        "target_states": [{"load": 9, "bri": 7500}],
        "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
        "scripts": ["test.py"],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/jobs", "post", response_json, request_json
    )

    job = Job(request_json, client_api_auth.auth)

    actual = await client_api_auth.async_create_job(job)

    assert isinstance(actual, Job)
    assert actual.id == 7
    assert actual.target_states[0]["bri"] == 7500


@pytest.mark.asyncio
async def test_async_get_job(client_api_auth, mock_aioresponse):
    """Test async_get_job."""
    response_json = {
        "status": "success",
        "data": {
            "id": 7,
            "target_states": [{"load": 9, "bri": 7500}],
            "flag_values": [{"flag": 39, "value": True}],
            "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
            "scripts": ["test.py"],
            "blocked_by": 10,
            "triggers": [5],
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/jobs/7", "get", response_json
    )

    actual = await client_api_auth.async_get_job(7)

    assert isinstance(actual, Job)
    assert actual.id == 7
    assert actual.target_states[0]["bri"] == 7500


@pytest.mark.asyncio
async def test_async_update_job(client_api_auth, mock_aioresponse):
    """Test async_update_job."""
    response_json = {
        "status": "success",
        "data": {
            "id": 7,
            "target_states": [{"load": 9, "bri": 7500}],
            "flag_values": [{"flag": 39, "value": True}],
            "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
            "scripts": ["test.py"],
            "blocked_by": 10,
            "triggers": [5],
        },
    }

    request_json = {
        "id": 7,
        "flag_values": [{"flag": 39, "value": True}],
        "target_states": [{"load": 9, "bri": 7500}],
        "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
        "scripts": ["test.py"],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/jobs/7", "put", response_json, request_json
    )
    job = Job(request_json, client_api_auth.auth)

    actual = await client_api_auth.async_update_job(job)

    assert isinstance(actual, Job)
    assert actual.id == 7
    assert actual.target_states[0]["bri"] == 7500


@pytest.mark.asyncio
async def test_async_delete_job(client_api_auth, mock_aioresponse):
    """Test async_delete_job."""
    response_json = {
        "status": "success",
        "data": {
            "id": 7,
            "target_states": [{"load": 9, "bri": 7500}],
            "flag_values": [{"flag": 39, "value": True}],
            "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
            "scripts": ["test.py"],
            "blocked_by": 10,
            "triggers": [5],
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/jobs/7", "delete", response_json
    )

    actual = await client_api_auth.async_delete_job(7)

    assert isinstance(actual, Job)
    assert actual.id == 7
    assert actual.target_states[0]["bri"] == 7500


@pytest.mark.asyncio
async def test_async_delete_job_loads(client_api_auth, mock_aioresponse):
    """Test async_delete_job_loads."""
    response_json = {"status": "success", "data": [69, 101]}
    request_json = {"loads": [69, 101]}

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/jobs/loads",
        "delete",
        response_json,
        request_json,
    )

    actual = await client_api_auth.async_delete_jobs_loads([69, 101])

    assert actual == response_json["data"]


@pytest.mark.asyncio
async def test_job_async_trigger(client_api_auth, mock_aioresponse):
    """Test job::async_trigger_*."""
    response_json = {
        "status": "success",
        "data": {
            "id": 7,
            "target_states": [{"load": 9, "bri": 7500}],
            "flag_values": [{"flag": 39, "value": True}],
            "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
            "scripts": ["test.py"],
            "blocked_by": 10,
            "triggers": [5],
        },
    }

    request_json = {
        "id": 7,
        "flag_values": [{"flag": 39, "value": True}],
        "target_states": [{"load": 9, "bri": 7500}],
        "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
        "scripts": ["test.py"],
    }

    job = Job(request_json, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/jobs/7/setflags",
        "get",
        response_json,
    )

    await job.async_trigger_flags()

    assert job.raw_data == response_json["data"]

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/jobs/7/run",
        "get",
        response_json,
    )

    await job.async_trigger_states()

    assert job.raw_data == response_json["data"]

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/jobs/7/ctrl",
        "get",
        response_json,
    )

    await job.async_trigger_ctrl()

    assert job.raw_data == response_json["data"]

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/jobs/7/execute",
        "get",
        response_json,
    )

    await job.async_trigger_scripts()

    assert job.raw_data == response_json["data"]

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/jobs/7/trigger",
        "get",
        response_json,
    )

    await job.async_trigger_all()

    assert job.raw_data == response_json["data"]


@pytest.mark.asyncio
async def test_job_async_trigger_button(client_api_auth, mock_aioresponse):
    """Test job::async_trigger_button."""
    response_json = {
        "status": "success",
        "data": {
            "id": 7,
            "target_states": [{"load": 9, "bri": 7500}],
            "flag_values": [{"flag": 39, "value": True}],
            "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
            "scripts": ["test.py"],
            "blocked_by": 10,
            "triggers": [5],
        },
    }

    request_json = {
        "id": 7,
        "flag_values": [{"flag": 39, "value": True}],
        "target_states": [{"load": 9, "bri": 7500}],
        "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
        "scripts": ["test.py"],
    }

    job = Job(request_json, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse,
        f"{BASE_URL}/jobs/7/ctrl/click/on",
        "get",
        response_json,
    )

    await job.async_trigger_button("click", "on")

    assert job.raw_data == response_json["data"]

    with pytest.raises(InvalidArgument, match="Invalid value"):
        await job.async_trigger_button("invalid", "on")

    with pytest.raises(InvalidArgument, match="Invalid value"):
        await job.async_trigger_button("click", "invalid")


@pytest.mark.asyncio
async def test_job_empty(client_api_auth, mock_aioresponse):
    """Test creating an empty job."""
    job = Job({}, client_api_auth.auth)
    assert job.id is None
    assert job.target_states == []
    assert job.flag_values == []
    assert job.button_ctrl is None
    assert job.scripts == []
    assert job.triggers == []


@pytest.mark.asyncio
async def test_job_async_refresh(client_api_auth, mock_aioresponse):
    """Test Job.async_refresh."""
    response_json = {
        "status": "success",
        "data": {
            "id": 7,
            "target_states": [{"load": 9, "bri": 7500}],
            "flag_values": [{"flag": 39, "value": True}],
            "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
            "scripts": ["test.py"],
            "blocked_by": 10,
            "triggers": [5],
        },
    }

    raw_data = {
        "id": 7,
        "target_states": [{"load": 9, "bri": 10000}],
        "flag_values": [{"flag": 39, "value": False}],
        "button_ctrl": {"event": "click", "button": "on", "loads": [11, 38]},
        "scripts": ["test.py"],
        "blocked_by": 10,
        "triggers": [5],
    }

    job = Job(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/jobs/7", "get", response_json
    )

    await job.async_refresh()

    assert job.id == 7
    assert job.target_states[0]["bri"] == 7500
    assert job.flag_values[0]["value"] is True
    assert job.button_ctrl["event"] == "click"
    assert job.scripts[0] == "test.py"
    assert job.blocked_by == 10
    assert job.triggers[0] == 5
