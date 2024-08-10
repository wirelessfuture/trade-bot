import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List
import pandas as pd


@dataclass
class CandleSeries:
    close: float  # Value of close price (shift from open price)
    ctm: datetime  # Candle start time in CET / CEST time zone
    ctmString: str  # String representation of the 'ctm' field
    high: float  # Highest value in the given period (shift from open price)
    low: float  # Lowest value in the given period (shift from open price)
    open: float  # Open price (in base currency * 10 to the power of digits)
    vol: float  # Volume in lots

    def __init__(self, entry: Dict[str, Any], digits: int) -> None:
        scaling_factor = 10**digits
        self.open = entry["open"] / scaling_factor
        self.close = self.open + (entry["close"] / scaling_factor)
        self.high = self.open + (entry["high"] / scaling_factor)
        self.low = self.open + (entry["low"] / scaling_factor)
        self.ctm = entry["ctm"]
        self.ctmString = entry["ctmString"]
        self.vol = entry["vol"]

    def to_series(self) -> pd.Series:
        """
        Converts the candle data to a pandas Series.

        :return: A pandas Series containing the candle data.
        """
        data: Dict[str, Any] = {
            "ctm": self.ctm,
            "ctmString": self.ctmString,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "vol": self.vol,
        }
        return pd.Series(data)


@dataclass
class CandleFrame:
    digits: int
    candles: List[CandleSeries] = field(default_factory=list)

    def __init__(self, data: Dict[str, Any]) -> None:
        self.digits = data["returnData"]["digits"]
        rate_infos: Dict[str, Any] = data["returnData"]["rateInfos"]
        self.candles = [CandleSeries(entry, self.digits) for entry in rate_infos]

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts all the candles in the series to a single pandas DataFrame.

        :return: A pandas DataFrame containing all the candle data.
        """
        data: Dict[str, Any] = {
            "ctm": [candle.ctm for candle in self.candles],
            "ctmString": [candle.ctmString for candle in self.candles],
            "open": [candle.open for candle in self.candles],
            "high": [candle.high for candle in self.candles],
            "low": [candle.low for candle in self.candles],
            "close": [candle.close for candle in self.candles],
            "vol": [candle.vol for candle in self.candles],
        }
        return pd.DataFrame(data)
