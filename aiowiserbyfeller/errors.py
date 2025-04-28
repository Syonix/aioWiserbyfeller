"""Aiowiserbyfeller errors."""


class AiowiserbyfellerException(Exception):
    """Base exception for aiowiserbyfeller."""


class UnauthorizedUser(AiowiserbyfellerException):
    """Username is not authorized."""


class TokenMissing(AiowiserbyfellerException):
    """Token is missing. Run claim first."""


class AuthorizationFailed(AiowiserbyfellerException):
    """Claim returned non-success error"""


class InvalidLoadType(AiowiserbyfellerException):
    """InvalidLoadType"""


class InvalidArgument(AiowiserbyfellerException):
    """InvalidArgument"""


class UnsuccessfulRequest(AiowiserbyfellerException):
    """Request returned non-success error"""


class WebsocketError(AiowiserbyfellerException):
    """Request returned non-success error"""
