import datetime
from dataclasses import dataclass, field
from typing import List, Any, Dict

from pandas import Series, DataFrame


@dataclass
class KLine:
    open_time: datetime.datetime
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: datetime.datetime
    quote_asset_volume: float
    number_of_trades: int
    taker_buy_base_asset_volume: float
    taker_buy_quote_asset_volume: float

    def __init__(self, entry: List[Any]) -> None:
        self.open_time = datetime.datetime.fromtimestamp(entry[0] / 1000.0)
        self.open = float(entry[1])
        self.high = float(entry[2])
        self.low = float(entry[3])
        self.close = float(entry[4])
        self.volume = float(entry[5])
        self.close_time = datetime.datetime.fromtimestamp(entry[6] / 1000.0)
        self.quote_asset_volume = float(entry[7])
        self.number_of_trades = int(entry[8])
        self.taker_buy_base_asset_volume = float(entry[9])
        self.taker_buy_quote_asset_volume = float(entry[10])

    def to_json(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "open_time": self.open_time,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
            "close_time": self.close_time,
            "quote_asset_volume": self.quote_asset_volume,
            "number_of_trades": self.number_of_trades,
            "taker_buy_base_asset_volume": self.taker_buy_base_asset_volume,
            "taker_buy_quote_asset_volume": self.taker_buy_quote_asset_volume,
        }
        return data

    def to_series(self) -> Series:
        return Series(self.to_json())


@dataclass
class KLines:
    klines: List[KLine] = field(default_factory=list)

    def __init__(self, data: List[List[Any]]) -> None:
        self.klines = [KLine(entry) for entry in data]

    def to_json(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "open_time": [kline.open_time for kline in self.klines],
            "open": [kline.open for kline in self.klines],
            "high": [kline.high for kline in self.klines],
            "low": [kline.low for kline in self.klines],
            "close": [kline.close for kline in self.klines],
            "volume": [kline.volume for kline in self.klines],
            "close_time": [kline.close_time for kline in self.klines],
            "quote_asset_volume": [kline.quote_asset_volume for kline in self.klines],
            "number_of_trades": [kline.number_of_trades for kline in self.klines],
            "taker_buy_base_asset_volume": [
                kline.taker_buy_base_asset_volume for kline in self.klines
            ],
            "taker_buy_quote_asset_volume": [
                kline.taker_buy_quote_asset_volume for kline in self.klines
            ],
        }
        return data

    def to_dataframe(self) -> DataFrame:
        df = DataFrame(self.to_json())
        df.set_index("open_time", inplace=True)

        return df
