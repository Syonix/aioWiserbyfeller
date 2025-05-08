"""Aiowiserbyfeller errors."""


class AiowiserbyfellerException(Exception):
    """Base exception for aiowiserbyfeller."""


class UnauthorizedUser(AiowiserbyfellerException):
    """Username is not authorized."""


class TokenMissing(AiowiserbyfellerException):
    """Token is missing. Run claim first."""


class AuthorizationFailed(AiowiserbyfellerException):
    """Claim returned non-success error."""


class InvalidLoadType(AiowiserbyfellerException):
    """InvalidLoadType."""


class InvalidArgument(AiowiserbyfellerException):
    """InvalidArgument."""


class UnsuccessfulRequest(AiowiserbyfellerException):
    """Request returned non-success response."""


class InvalidJson(UnsuccessfulRequest):
    """Request returned invalid JSON."""

    def __init__(
        self,
        msg="Response is not valid JSON. Are you sure, you're connecting to a Wiser µGateway?",
        *args,
    ):
        """Initialize an invalid JSON exception."""
        super().__init__(msg, *args)


class WebsocketError(AiowiserbyfellerException):
    """Request returned non-success error."""
