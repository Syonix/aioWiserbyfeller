"""aiowiserbyfeller Api class scene tests."""

import pytest

from aiowiserbyfeller import Scene

from .conftest import BASE_URL, prepare_test_authenticated  # noqa: TID251


@pytest.mark.asyncio
async def test_async_get_scenes(client_api_auth, mock_aioresponse):
    """Test async_get_scenes."""
    response_json = {
        "status": "success",
        "data": [
            {
                "job": 14,
                "type": 0,
                "name": "Abwesend",
                "kind": 1,
                "id": 15,
                "sceneButtons": [
                    {"id": 13, "title": "Szenentaste 1", "description": "ID • 13"}
                ],
            }
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/scenes", "get", response_json
    )

    actual = await client_api_auth.async_get_scenes()

    assert len(actual) == 1
    assert isinstance(actual[0], Scene)
    assert actual[0].id == 15
    assert actual[0].scene_buttons[0]["title"] == "Szenentaste 1"


@pytest.mark.asyncio
async def test_async_create_scene(client_api_auth, mock_aioresponse):
    """Test async_create_scene."""
    response_json = {
        "status": "success",
        "data": {
            "job": 14,
            "type": 0,
            "name": "Abwesend",
            "kind": 1,
            "id": 15,
            "sceneButtons": [],
        },
    }

    request_json = {
        "job": 14,
        "type": 0,
        "name": "Abwesend",
        "kind": 1,
        "sceneButtons": [],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/scenes", "post", response_json, request_json
    )

    scene = Scene(request_json, client_api_auth.auth)

    actual = await client_api_auth.async_create_scene(scene)

    assert isinstance(actual, Scene)
    assert actual.id == 15
    assert actual.name == "Abwesend"


@pytest.mark.asyncio
async def test_async_get_scene(client_api_auth, mock_aioresponse):
    """Test async_get_scene."""
    response_json = {
        "status": "success",
        "data": {
            "job": 14,
            "type": 0,
            "name": "Abwesend",
            "kind": 1,
            "id": 15,
            "sceneButtons": [
                {"id": 13, "title": "Szenentaste 1", "description": "ID • 13"}
            ],
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/scenes/15", "get", response_json
    )

    actual = await client_api_auth.async_get_scene(15)

    assert isinstance(actual, Scene)
    assert actual.id == 15
    assert actual.scene_buttons[0]["title"] == "Szenentaste 1"


@pytest.mark.asyncio
async def test_async_update_scene(client_api_auth, mock_aioresponse):
    """Test async_update_scene."""
    response_json = {
        "status": "success",
        "data": {
            "job": 14,
            "type": 0,
            "name": "Abwesend",
            "kind": 1,
            "id": 15,
            "sceneButtons": [
                {"id": 13, "title": "Szenentaste 1", "description": "ID • 13"}
            ],
        },
    }

    request_json = {
        "job": 14,
        "type": 0,
        "name": "Abwesend",
        "kind": 1,
        "id": 15,
        "sceneButtons": [
            {"id": 13, "title": "Szenentaste 1", "description": "ID • 13"}
        ],
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/scenes/15", "put", response_json, request_json
    )
    scene = Scene(request_json, client_api_auth.auth)
    scene = await client_api_auth.async_update_scene(scene)

    assert scene.id == 15
    assert scene.scene_buttons[0]["title"] == "Szenentaste 1"


@pytest.mark.asyncio
async def test_scene_async_refresh(client_api_auth, mock_aioresponse):
    """Test Scene.async_refresh."""
    response_json = {
        "status": "success",
        "data": {
            "job": 12,
            "type": 0,
            "name": "Abwesend Neu",
            "kind": 1,
            "id": 15,
            "sceneButtons": [
                {"id": 13, "title": "Szenentaste 2", "description": "ID • 13"}
            ],
        },
    }

    raw_data = {
        "job": 14,
        "type": 0,
        "name": "Abwesend",
        "kind": 1,
        "id": 15,
        "sceneButtons": [
            {"id": 13, "title": "Szenentaste 1", "description": "ID • 13"}
        ],
    }

    scene = Scene(raw_data, client_api_auth.auth)

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/scenes/15", "get", response_json
    )

    await scene.async_refresh()

    assert scene.id == 15
    assert scene.job == 12
    assert scene.type == 0
    assert scene.name == "Abwesend Neu"
    assert scene.kind == 1
    assert scene.scene_buttons[0]["title"] == "Szenentaste 2"


@pytest.mark.asyncio
async def test_async_delete_scene(client_api_auth, mock_aioresponse):
    """Test async_delete_scene."""
    response_json = {
        "status": "success",
        "data": {
            "job": 14,
            "type": 0,
            "name": "Abwesend",
            "kind": 1,
            "id": 15,
            "sceneButtons": [
                {"id": 13, "title": "Szenentaste 1", "description": "ID • 13"}
            ],
        },
    }

    await prepare_test_authenticated(
        mock_aioresponse, f"{BASE_URL}/scenes/15", "delete", response_json
    )

    actual = await client_api_auth.async_delete_scene(15)

    assert isinstance(actual, Scene)
    assert actual.id == 15
