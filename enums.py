from enum import Enum


class Interval(Enum):
    SECOND_1 = "1s"
    MINUTE_1 = "1m"
    MINUTE_3 = "3m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    HOUR_1 = "1h"
    HOUR_2 = "2h"
    HOUR_4 = "4h"
    HOUR_6 = "6h"
    HOUR_8 = "8h"
    HOUR_12 = "12h"
    DAY_1 = "1d"
    DAY_3 = "3d"
    WEEK_1 = "1w"
    MONTH_1 = "1M"


class OrderStatus(Enum):
    NEW = 0
    PENDING_NEW = 1
    PARTIALLY_FILLED = 2
    FILLED = 3
    CANCELLED = 4
    PENDING_CANCEL = 5
    REJECTED = 6
    EXPIRED = 7
    EXPIRED_IN_MATCH = 8


class OrderType(Enum):
    LIMIT = 0
    MARKET = 1
    STOP_LOSS = 2
    STOP_LOSS_LIMIT = 3
    TAKE_PROFIT = 4
    TAKE_PROFIT_LIMIT = 5
    LIMIT_MAKER = 6


class OrderSide(Enum):
    BUY = 0
    SELL = 1


class TimeInForce(Enum):
    GTC = 0 # Good Til Cancelled
    IOC = 1 # Immediate Or Cancel
    FOK = 2 # Fill Or Kill
