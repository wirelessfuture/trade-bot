from abc import ABC
from typing import List, Literal

from pandas import DataFrame
import signals
from data_classes import KLines


class BaseStrategy(ABC):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        allow_short: bool = False,
    ) -> None:
        self.klines: KLines = klines
        self.df: DataFrame = klines.to_dataframe()
        self.balance: float = initial_balance
        self.allow_short: bool = allow_short
        self.long_position: int = 0
        self.short_position: int = 0
        self.trade_log: list = []
        self.signal_df: DataFrame = None
        self.signal: signals.BaseSignal = None

    def apply_strategy(self) -> None:
        for _, row in self.signal_df.iterrows():
            if row[self.signal.name] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)
                self.buy(row["close"], row.name)
            elif row[self.signal.name] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)
                elif self.allow_short:
                    self.sell(row["close"], row.name)

    def buy(self, price, timestamp) -> None:
        if self.long_position == 0:
            self.long_position = self.balance / price
            self.balance = 0
            self.trade_log.append(
                (timestamp, "BUY", price, self.long_position, self.balance)
            )

    def sell(self, price, timestamp) -> None:
        if self.long_position > 0:
            self.balance = self.long_position * price
            self.long_position = 0
            self.trade_log.append(
                (timestamp, "SELL", price, self.long_position, self.balance)
            )
        elif self.allow_short and self.short_position == 0:
            self.short_position = self.balance / price
            self.balance = 0
            self.trade_log.append(
                (timestamp, "SHORT", price, self.short_position, self.balance)
            )
        elif self.short_position > 0:
            self.balance = self.short_position * price
            self.short_position = 0
            self.trade_log.append(
                (timestamp, "COVER", price, self.short_position, self.balance)
            )

    def get_trade_log(self) -> DataFrame:
        return DataFrame(
            self.trade_log,
            columns=["timestamp", "action", "price", "position", "balance"],
        )


class CombinedStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        strategies: List[BaseStrategy],
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.strategies = strategies

    def apply_combined_strategy(self) -> None:
        combined_signals = DataFrame(index=self.df.index)

        for strategy in self.strategies:
            strategy.apply_strategy()
            signals = strategy.get_trade_log()
            signals = signals.set_index("timestamp")[["action"]]
            signals.columns = [type(strategy).__name__]
            combined_signals = combined_signals.join(signals, how="outer")

        combined_signals["combined_signal"] = combined_signals.apply(
            self.combine_signals, axis=1
        )

        for index, row in combined_signals.iterrows():
            if row["combined_signal"] == "BUY":
                if self.short_position > 0:
                    self.sell(self.df.loc[index, "close"], index)
                self.buy(self.df.loc[index, "close"], index)
            elif row["combined_signal"] == "SELL":
                if self.long_position > 0:
                    self.sell(self.df.loc[index, "close"], index)
                elif self.allow_short:
                    self.sell(self.df.loc[index, "close"], index)

    @staticmethod
    def combine_signals(row) -> Literal["BUY", "SELL", "HOLD"]:
        buy_count: int = (row == "BUY").sum()
        sell_count: int = (row == "SELL").sum()

        if buy_count > sell_count:
            return "BUY"
        elif sell_count > buy_count:
            return "SELL"
        else:
            return "HOLD"


class RSIStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        rsi_period: int = 14,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.RSISignal(klines, rsi_period)
        self.signal_df = self.signal.generate()


class MACDStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        macd_fast: int = 12,
        macd_slow: int = 26,
        macd_signal: int = 9,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.MACDSignal(klines, macd_fast, macd_slow, macd_signal)
        self.signal_df = self.signal.generate()


class StochasticStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        k_window: int = 14,
        d_window: int = 3,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.StochasticSignal(klines, k_window, d_window)
        self.signal_df = self.signal.generate()


class TSIStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window_slow: int = 25,
        window_fast: int = 13,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.TSISignal(klines, window_slow, window_fast)
        self.signal_df = self.signal.generate()


class UltimateOscillatorStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window1: int = 7,
        window2: int = 14,
        window3: int = 28,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.UltimateOscillatorSignal(
            klines, window1, window2, window3
        )
        self.signal_df = self.signal.generate()


class WilliamsRStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        lbp: int = 14,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.WilliamsRSignal(klines, lbp)
        self.signal_df = self.signal.generate()


class AwesomeOscillatorStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window1: int = 5,
        window2: int = 34,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.AwesomeOscillatorSignal(klines, window1, window2)
        self.signal_df = self.signal.generate()


class ADXStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 14,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.ADXSignal(klines, window)
        self.signal_df = self.signal.generate()


class AroonStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 25,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.AroonSignal(klines, window)
        self.signal_df = self.signal.generate()


class CCIStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 20,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.CCISignal(klines, window)
        self.signal_df = self.signal.generate()


class BollingerBandsStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 20,
        window_dev: int = 2,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.BollingerBandsSignal(klines, window, window_dev)
        self.signal_df = self.signal.generate()


class KeltnerChannelStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 20,
        window_atr: int = 10,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.KeltnerChannelSignal(klines, window, window_atr)
        self.signal_df = self.signal.generate()


class DonchianChannelStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 20,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.DonchianChannelSignal(klines, window)
        self.signal_df = self.signal.generate()


class ATRStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 14,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.ATRSignal(klines, window)
        self.signal_df = self.signal.generate()


class OBVStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.OBVSignal(klines)
        self.signal_df = self.signal.generate()


class CMFStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 20,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.CMFSignal(klines, window)
        self.signal_df = self.signal.generate()


class MFIStrategy(BaseStrategy):
    def __init__(
        self,
        klines: KLines,
        initial_balance: float,
        window: int = 14,
        allow_short: bool = False,
    ) -> None:
        super().__init__(klines, initial_balance, allow_short)
        self.signal = signals.MFISignal(klines, window)
        self.signal_df = self.signal.generate()
