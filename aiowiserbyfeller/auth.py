"""Wrapper for authenticated API calls."""
from aiohttp import ClientSession
from .errors import AuthorizationFailed, TokenMissing, UnsuccessfulRequest


class Auth:
    """Class to make authenticated requests."""

    def __init__(self, http: ClientSession, host: str, **kwargs):
        """Initialize.

        Args:
            http: ClientSession instance to be used
            host: Hostname or IP of µGateway
            user: Username to be used for claiming token
        """
        self.http = http
        self.base_url = "http://" + host + "/api"
        self.host = host
        self.access_token = kwargs.get("token", None)

    async def claim(self, user: str, source="installer", **kwargs) -> str:
        """
        Get authentication token.

        As soon you start the request the physical buttons of the Wiser
        µGateway will start flashing purple and pink for 30 seconds. For
        a valid request, one of the physical buttons has to be pressed
        within 30 seconds!

        Warning: Claiming the same user again invalidates a previous token.

        See https://github.com/Feller-AG/wiser-tutorial/blob/main/doc/authentication.md

        Args:
            user: User type like "installer", "admin" or "enduser"
            source: Source user type where this account will be copied from
        """

        data = {"user": user}

        if source is not None:
            data["source"] = source

        resp = await self.http.request(
            "post", f"{self.base_url}/account/claim", **kwargs, json=data
        )
        json = await resp.json()

        if json["status"] != "success":
            raise AuthorizationFailed(json["message"])

        self.access_token = json["data"]["secret"]

        return self.access_token

    async def request(self, method: str, path: str, **kwargs):
        """Send a request to the API."""
        headers = kwargs.get("headers")
        require_token = kwargs.pop("require_token", True)

        if require_token and self.access_token is None:
            raise TokenMissing

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        if self.access_token is not None:
            headers["authorization"] = "Bearer: " + self.access_token

        resp = await self.http.request(
            method,
            f"{self.base_url}/{path}",
            **kwargs,
            headers=headers,
        )

        resp.raise_for_status()
        json = await resp.json()

        if json["status"] == "error" and "api is locked" in json["message"]:
            raise TokenMissing()

        if json["status"] != "success":
            raise UnsuccessfulRequest(json["message"])

        return json["data"]

    async def is_valid_login(self) -> bool:
        """Check if current token is valid."""
        try:
            data = await self.request("get", "account")
            return "user" in data
        except UnsuccessfulRequest:
            return False
