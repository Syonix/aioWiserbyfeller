"""Wrapper for authenticated API calls."""

import json

from aiohttp import ClientSession, ContentTypeError

from .errors import (
    AuthorizationFailed,
    InvalidJson,
    TokenMissing,
    UnauthorizedUser,
    UnsuccessfulRequest,
)


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, http: ClientSession, host: str, **kwargs):
        """Initialize an auth object.

        Args:
            http: ClientSession instance to be used
            host: Hostname or IP of µGateway
            user: Username to be used for claiming token
            kwargs: Can contain the token if applicable

        """
        self.http = http
        self.base_url = f"http://{host}/api"
        self.host = host
        self.access_token = kwargs.get("token")

    async def claim(self, user: str, source="installer", **kwargs) -> str:
        """Get authentication token.

        As soon you start the request the physical buttons of the Wiser
        µGateway will start flashing purple and pink for 30 seconds. For
        a valid request, one of the physical buttons has to be pressed
        within 30 seconds!

        Warning: Claiming the same user again invalidates a previous token.

        See https://github.com/Feller-AG/wiser-tutorial/blob/main/doc/authentication.md

        Args:
            user: User type like "installer", "admin" or "enduser"
            source: Source user type where this account will be copied from
            kwargs: Are forwarded to http.request call.

        """

        data = {"user": user}

        if source is not None:
            data["source"] = source

        resp = await self.http.request(
            "post", f"{self.base_url}/account/claim", **kwargs, json=data
        )

        try:
            parsed = await resp.json()
        except (json.JSONDecodeError, ContentTypeError) as e:
            raise InvalidJson from e

        if parsed["status"] != "success":
            raise AuthorizationFailed(parsed["message"])

        self.access_token = parsed["data"]["secret"]

        return self.access_token

    async def request(self, method: str, path: str, **kwargs):
        """Send a request to the API."""
        headers = kwargs.pop("headers", {})
        require_token = kwargs.pop("require_token", True)

        if require_token and self.access_token is None:
            raise TokenMissing

        if self.access_token is not None:
            headers["authorization"] = "Bearer: " + self.access_token

        resp = await self.http.request(
            method,
            f"{self.base_url}/{path}",
            **kwargs,
            headers=headers,
        )

        resp.raise_for_status()

        try:
            parsed = await resp.json()
        except (json.JSONDecodeError, ContentTypeError) as e:
            raise InvalidJson from e

        if parsed["status"] == "error" and "api is locked" in parsed["message"]:
            raise TokenMissing

        if parsed["status"] == "error" and parsed["message"] == "unauthorized user":
            raise UnauthorizedUser

        if parsed["status"] != "success":
            raise UnsuccessfulRequest(parsed["message"])

        return parsed["data"]

    async def is_valid_login(self) -> bool:
        """Check if current token is valid."""
        try:
            data = await self.request("get", "account")
            return "user" in data  # noqa: TRY300
        except UnsuccessfulRequest:
            return False
