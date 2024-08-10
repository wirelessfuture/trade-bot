class APIError(Exception):
    """Base class for all API exceptions."""

    def __init__(self, message: str = "An API error occurred"):
        super().__init__(message)


class InvalidPriceError(APIError):
    def __init__(self):
        super().__init__("Invalid price")


class InvalidStopLossOrTakeProfitError(APIError):
    def __init__(self):
        super().__init__("Invalid StopLoss or TakeProfit")


class InvalidVolumeError(APIError):
    def __init__(self):
        super().__init__("Invalid volume")


class LoginDisabledError(APIError):
    def __init__(self):
        super().__init__("Login disabled")


class InvalidLoginOrPasswordError(APIError):
    def __init__(self):
        super().__init__("Invalid login or password")


class MarketClosedError(APIError):
    def __init__(self):
        super().__init__("Market for instrument is closed")


class MismatchedParametersError(APIError):
    def __init__(self):
        super().__init__("Mismatched parameters")


class ModificationDeniedError(APIError):
    def __init__(self):
        super().__init__("Modification is denied")


class NotEnoughMoneyError(APIError):
    def __init__(self):
        super().__init__("Not enough money on account to perform trade")


class OffQuotesError(APIError):
    def __init__(self):
        super().__init__("Off quotes")


class OppositePositionsProhibitedError(APIError):
    def __init__(self):
        super().__init__("Opposite positions prohibited")


class ShortPositionsProhibitedError(APIError):
    def __init__(self):
        super().__init__("Short positions prohibited")


class PriceChangedError(APIError):
    def __init__(self):
        super().__init__("Price has changed")


class RequestTooFrequentError(APIError):
    def __init__(self):
        super().__init__("Request too frequent")


class TooManyTradeRequestsError(APIError):
    def __init__(self):
        super().__init__("Too many trade requests")


class TradingDisabledError(APIError):
    def __init__(self):
        super().__init__("Trading on instrument disabled")


class TradingTimeoutError(APIError):
    def __init__(self):
        super().__init__("Trading timeout")


class SymbolDoesNotExistError(APIError):
    def __init__(self):
        super().__init__("Symbol does not exist for given account")


class CannotTradeOnSymbolError(APIError):
    def __init__(self):
        super().__init__("Account cannot trade on given symbol")


class PendingOrderCannotBeClosedError(APIError):
    def __init__(self):
        super().__init__(
            "Pending order cannot be closed. Pending order must be deleted"
        )


class CannotCloseAlreadyClosedOrderError(APIError):
    def __init__(self):
        super().__init__("Cannot close already closed order")


class NoSuchTransactionError(APIError):
    def __init__(self):
        super().__init__("No such transaction")


class UnknownInstrumentSymbolError(APIError):
    def __init__(self):
        super().__init__("Unknown instrument symbol")


class UnknownTransactionTypeError(APIError):
    def __init__(self):
        super().__init__("Unknown transaction type")


class UserNotLoggedError(APIError):
    def __init__(self):
        super().__init__("User is not logged")


class MethodDoesNotExistError(APIError):
    def __init__(self):
        super().__init__("Method does not exist")


class IncorrectPeriodError(APIError):
    def __init__(self):
        super().__init__("Incorrect period given")


class MissingDataError(APIError):
    def __init__(self):
        super().__init__("Missing data")


class IncorrectCommandFormatError(APIError):
    def __init__(self):
        super().__init__("Incorrect command format")


class InvalidTokenError(APIError):
    def __init__(self):
        super().__init__("Invalid token")


class UserAlreadyLoggedError(APIError):
    def __init__(self):
        super().__init__("User already logged")


class SessionTimedOutError(APIError):
    def __init__(self):
        super().__init__("Session timed out")


class InvalidParametersError(APIError):
    def __init__(self):
        super().__init__("Invalid parameters")


class InternalError(APIError):
    def __init__(self):
        super().__init__("Internal error, please contact support")


class RequestTimedOutError(APIError):
    def __init__(self):
        super().__init__("Internal error, request timed out")


class IncorrectLoginCredentialsError(APIError):
    def __init__(self):
        super().__init__(
            "Login credentials are incorrect or this login is not allowed to use an application with this appId"
        )


class SystemOverloadedError(APIError):
    def __init__(self):
        super().__init__("Internal error, system overloaded")


class NoAccessError(APIError):
    def __init__(self):
        super().__init__("No access")


class ConnectionLimitReachedError(APIError):
    def __init__(self):
        super().__init__("You have reached the connection limit")


class DataLimitExceededError(APIError):
    def __init__(self):
        super().__init__("Data limit potentially exceeded")


class LoginBlacklistedError(APIError):
    def __init__(self):
        super().__init__("Your login is on the black list")


class CommandNotAllowedError(APIError):
    def __init__(self):
        super().__init__("You are not allowed to execute this command")


class IncorrectCustomTagReturned(APIError):
    def __init__(self):
        super().__init__("The customTag sent did not match the response")


ERROR_CODE_MAP = {
    "BE001": InvalidPriceError,
    "BE002": InvalidStopLossOrTakeProfitError,
    "BE003": InvalidVolumeError,
    "BE004": LoginDisabledError,
    "BE005": InvalidLoginOrPasswordError,
    "BE006": MarketClosedError,
    "BE007": MismatchedParametersError,
    "BE008": ModificationDeniedError,
    "BE009": NotEnoughMoneyError,
    "BE010": OffQuotesError,
    "BE011": OppositePositionsProhibitedError,
    "BE012": ShortPositionsProhibitedError,
    "BE013": PriceChangedError,
    "BE014": RequestTooFrequentError,
    "BE016": TooManyTradeRequestsError,
    "BE017": TooManyTradeRequestsError,
    "BE018": TradingDisabledError,
    "BE019": TradingTimeoutError,
    "BE020": InternalError,
    "BE021": InternalError,
    "BE022": InternalError,
    "BE023": InternalError,
    "BE024": InternalError,
    "BE025": InternalError,
    "BE026": InternalError,
    "BE027": InternalError,
    "BE028": InternalError,
    "BE029": InternalError,
    "BE030": InternalError,
    "BE031": InternalError,
    "BE032": InternalError,
    "BE033": InternalError,
    "BE034": InternalError,
    "BE035": InternalError,
    "BE036": InternalError,
    "BE037": InternalError,
    "BE099": InternalError,
    "BE094": SymbolDoesNotExistError,
    "BE095": CannotTradeOnSymbolError,
    "BE096": PendingOrderCannotBeClosedError,
    "BE097": CannotCloseAlreadyClosedOrderError,
    "BE098": NoSuchTransactionError,
    "BE101": UnknownInstrumentSymbolError,
    "BE102": UnknownTransactionTypeError,
    "BE103": UserNotLoggedError,
    "BE104": MethodDoesNotExistError,
    "BE105": IncorrectPeriodError,
    "BE106": MissingDataError,
    "BE110": IncorrectCommandFormatError,
    "BE115": SymbolDoesNotExistError,
    "BE116": SymbolDoesNotExistError,
    "BE117": InvalidTokenError,
    "BE118": UserAlreadyLoggedError,
    "BE200": SessionTimedOutError,
    "EX000": InvalidParametersError,
    "EX001": InternalError,
    "EX002": InternalError,
    "SExxx": InternalError,
    "BE000": InternalError,
    "EX003": RequestTimedOutError,
    "EX004": IncorrectLoginCredentialsError,
    "EX005": SystemOverloadedError,
    "EX006": NoAccessError,
    "EX007": InvalidLoginOrPasswordError,
    "EX008": ConnectionLimitReachedError,
    "EX009": DataLimitExceededError,
    "EX010": LoginBlacklistedError,
    "EX011": CommandNotAllowedError,
    "CA001": IncorrectCustomTagReturned,
}


def raise_api_error(error_code: str) -> None:
    if error_code.startswith("SE"):
        raise ERROR_CODE_MAP.get("SExxx", APIError)
    raise ERROR_CODE_MAP.get(error_code, APIError)
