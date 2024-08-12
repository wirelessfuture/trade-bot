from time import time
from typing import List, Any

from binance.spot import Spot
from data_classes import KLines
from enums import Interval
from constants import (
    BINANCE_TESTNET_API_KEY,
    BINANCE_TESTNET_API_SECRET,
    BINANCE_TRADE_CURRENCY,
    BINANCE_TESTNET_DATA_URL,
)
from strategies import RSIStrategy, MACDStrategy, CombinedStrategy


if __name__ == "__main__":
    data_client = Spot(
        api_key=BINANCE_TESTNET_API_KEY,
        api_secret=BINANCE_TESTNET_API_SECRET,
        base_url=BINANCE_TESTNET_DATA_URL,
    )

    symbol = f"ETH{BINANCE_TRADE_CURRENCY}"
    interval = Interval.MINUTE_30.value
    start_time = int((time() - 10080 * 60) * 1000)
    end_time = int((time()) * 1000)
    initial_balance = 10000

    new_kline_data: List[List[Any]] = data_client.klines(
        symbol=symbol,
        interval=interval,
        startTime=start_time,
        endTime=end_time,
    )

    new_klines: KLines = KLines(data=new_kline_data)

    rsi = RSIStrategy(
        klines=new_klines,
        initial_balance=initial_balance,
        allow_short=False,
    )

    macd = MACDStrategy(
        klines=new_klines,
        initial_balance=initial_balance,
        allow_short=False,
    )

    combined_strategy = CombinedStrategy(
        klines=new_klines, initial_balance=initial_balance, strategies=[rsi, macd]
    )
    combined_strategy.apply_combined_strategy()
    print(combined_strategy.get_trade_log())
    print(new_klines.to_dataframe())