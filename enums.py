from enum import Enum


class Period(Enum):
    PERIOD_M1 = 1
    PERIOD_M5 = 5
    PERIOD_M15 = 15
    PERIOD_M30 = 30
    PERIOD_H1 = 60
    PERIOD_H4 = 240
    PERIOD_D1 = 1440
    PERIOD_W1 = 10080
    PERIOD_MN1 = 43200


class TradeCommand(Enum):
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5


class TradeType(Enum):
    OPEN = 0
    CLOSE = 2
    MODIFY = 3
    DELETE = 4


class TradeStatus(Enum):
    ERROR = 0
    PENDING = 1
    ACCEPTED = 3
    REJECTED = 4
