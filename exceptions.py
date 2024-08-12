class APIError(Exception):
    """Base class for all API exceptions."""

    def __init__(self, message: str = "An API error occurred"):
        super().__init__(message)


ERROR_CODE_MAP = {}


def raise_api_error(error_code: str) -> None:
    raise ERROR_CODE_MAP.get(error_code, APIError)
