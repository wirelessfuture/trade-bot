from abc import ABCMeta, abstractmethod
from typing import Literal, List, Dict, Any
from uuid import uuid4

from logger import logger
from exceptions import raise_api_error
from xtb_api_connector import APIClient


class BaseCommand(metaclass=ABCMeta):
    COMMAND = None

    @abstractmethod
    def __init__(
        self,
        arguments: Dict[str, Any],
        client: APIClient,
    ) -> None:
        assert isinstance(arguments, dict | None), logger.error(
            f"Arguments must be dict or None but got {type(arguments)}"
        )

        self.validate_arguments(arguments)

        self.arguments: dict = arguments if arguments else dict()
        self._client: APIClient = client

    @abstractmethod
    def validate_arguments(self) -> None:
        pass

    def payload(self) -> dict[Literal["command", "arguments"], str | dict]:
        return dict([("command", self.COMMAND), ("arguments", self.arguments)])

    def execute(self) -> dict:
        self.custom_tag = str(uuid4())
        payload = self.payload()
        payload["customTag"] = self.custom_tag

        response: Dict[str, Any] = self._client.execute(payload)
        if not response["status"]:
            logger.error(
                f"Error code: {response.get('errorCode')}, Error description: {response.get('errorDescr')}"
            )
            raise_api_error(response["errorCode"])
        elif response["customTag"] != self.custom_tag:
            logger.error(
                f"customTag {response.get('customTag')} in response does not match {self.custom_tag} from request"
            )
            raise_api_error("CE001")
        return response


class LoginCommand(BaseCommand):
    COMMAND = "login"

    def __init__(self, arguments: Dict[str, Any], client: APIClient) -> None:
        super().__init__(arguments, client)

    def validate_arguments(self, arguments: Dict[str, Any]) -> None:
        required_fields: List[str] = ["userId", "password"]
        for field in required_fields:
            if field not in arguments:
                raise ValueError(f"Missing required argument: {field}")

            if not isinstance(arguments[field], str):
                raise ValueError(
                    f"{field} must be a string, got {type(arguments[field])}"
                )

        optional_fields: List[str] = ["appId", "appName"]
        for field in optional_fields:
            if field in arguments and not isinstance(arguments[field], str):
                raise ValueError(
                    f"{field} must be a string if provided, got {type(arguments[field])}"
                )


class GetSymbol(BaseCommand):
    COMMAND = "getSymbol"

    def __init__(self, arguments: Dict[str, Any], client: APIClient) -> None:
        super().__init__(arguments, client)

    def validate_arguments(self, arguments: Dict[str, Any]) -> None:
        required_fields: List[str] = ["symbol"]
        for field in required_fields:
            if field not in arguments:
                raise ValueError(f"Missing required argument: {field}")

        symbol = arguments.get("symbol")

        if not isinstance(symbol, str) or symbol is None:
            raise ValueError(
                f"Symbol must be a str and cannot be None, got {type(symbol)}"
            )


class GetChartRangeRequestCommand(BaseCommand):
    COMMAND = "getChartRangeRequest"

    def __init__(
        self,
        arguments: Dict[str, Any],
        client: APIClient,
    ) -> None:
        super().__init__(arguments, client)

    def validate_arguments(self, arguments: Dict[str, Any]) -> None:
        arguments = arguments.get("info")

        required_fields: List[str] = ["period", "start", "symbol"]
        for field in required_fields:
            if field not in arguments:
                raise ValueError(f"Missing required argument: {field}")

        period = arguments.get("period")
        start = arguments.get("start")
        end = arguments.get("end")
        ticks = arguments.get("ticks", 0)

        if not isinstance(period, int) or period <= 0:
            raise ValueError(f"Period must be a positive integer, got {period}")

        if not isinstance(start, int):
            raise ValueError(f"Start must be an int, got {type(start)}")

        if end is not None and not isinstance(end, int):
            raise ValueError(f"End must be an int if provided, got {type(end)}")

        if not isinstance(arguments.get("symbol"), str):
            raise ValueError(
                f"Symbol must be a string, got {type(arguments.get('symbol'))}"
            )

        if not isinstance(ticks, int):
            raise ValueError(f"Ticks must be an integer, got {type(ticks)}")

        if ticks == 0:
            if end is None:
                raise ValueError(
                    "End time must be provided when ticks is 0 or not set."
                )
        else:
            arguments.pop("end", None)
            if ticks > 0:
                logger.info(f"API will return {ticks} candles from start time {start}")
            elif ticks < 0:
                logger.info(f"API will return {-ticks} candles to start time {start}")
