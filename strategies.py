import pandas as pd
from abc import ABC, abstractmethod
from typing import List

import signals
from data_classes import CandleFrame


class BaseStrategy(ABC):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        allow_short: bool = False,
    ):
        self.candle_frame = candle_frame
        self.df = candle_frame.to_dataframe()
        self.balance = initial_balance
        self.long_position = 0  # Current long position
        self.short_position = 0  # Current short position
        self.allow_short = allow_short  # Flag to allow short positions
        self.trade_log = []  # Log of trades

    @abstractmethod
    def apply_strategy(self):
        pass

    def buy(self, price, timestamp):
        if self.long_position == 0:  # Only buy if no current long position
            self.long_position = self.balance / price  # Buy with entire balance
            self.balance = 0  # All money is now in the position
            self.trade_log.append(
                (timestamp, "BUY", price, self.long_position, self.balance)
            )

    def sell(self, price, timestamp):
        if self.long_position > 0:  # Only sell if holding a long position
            self.balance = self.long_position * price  # Sell all positions
            self.long_position = 0  # No more position
            self.trade_log.append(
                (timestamp, "SELL", price, self.long_position, self.balance)
            )
        elif (
            self.allow_short and self.short_position == 0
        ):  # Enter short position if allowed
            self.short_position = self.balance / price  # Short with entire balance
            self.balance = 0  # All money is now in the short position
            self.trade_log.append(
                (timestamp, "SHORT", price, self.short_position, self.balance)
            )
        elif self.short_position > 0:  # Cover short position
            self.balance = self.short_position * price  # Cover all short positions
            self.short_position = 0  # No more short position
            self.trade_log.append(
                (timestamp, "COVER", price, self.short_position, self.balance)
            )

    def get_trade_log(self):
        return pd.DataFrame(
            self.trade_log,
            columns=["timestamp", "action", "price", "position", "balance"],
        )


class CombinedStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        strategies: List[BaseStrategy],
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.strategies = strategies

    def apply_strategy(self):
        combined_signals = pd.DataFrame(index=self.df.index)

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
                    self.sell(
                        self.df.loc[index, "close"], index
                    )  # Cover short position
                self.buy(self.df.loc[index, "close"], index)  # Enter long position
            elif row["combined_signal"] == "SELL":
                if self.long_position > 0:
                    self.sell(self.df.loc[index, "close"], index)  # Exit long position
                elif self.allow_short:
                    self.sell(
                        self.df.loc[index, "close"], index
                    )  # Enter short position

    @staticmethod
    def combine_signals(row):
        buy_count = (row == "BUY").sum()
        sell_count = (row == "SELL").sum()

        if buy_count > sell_count:
            return "BUY"
        elif sell_count > buy_count:
            return "SELL"
        else:
            return "HOLD"


class RSIStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        rsi_period: int = 14,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.rsi_signal = signals.RSISignal(candle_frame, rsi_period)

    def apply_strategy(self):
        # Generate RSI signals
        signal_df = self.rsi_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["RSI_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["RSI_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class MACDStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        macd_fast: int = 12,
        macd_slow: int = 26,
        macd_signal: int = 9,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.macd_signal = signals.MACDSignal(
            candle_frame, macd_fast, macd_slow, macd_signal
        )

    def apply_strategy(self):
        # Generate MACD signals
        signal_df = self.macd_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["MACD_strategy_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["MACD_strategy_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class StochasticStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        k_window: int = 14,
        d_window: int = 3,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.stochastic_signal = signals.StochasticSignal(
            candle_frame, k_window, d_window
        )

    def apply_strategy(self):
        # Generate Stochastic signals
        signal_df = self.stochastic_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["Stoch_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["Stoch_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class TSIStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window_slow: int = 25,
        window_fast: int = 13,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.tsi_signal = signals.TSISignal(candle_frame, window_slow, window_fast)

    def apply_strategy(self):
        # Generate TSI signals
        signal_df = self.tsi_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["TSI_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["TSI_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class UltimateOscillatorStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window1: int = 7,
        window2: int = 14,
        window3: int = 28,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.ultimate_oscillator_signal = signals.UltimateOscillatorSignal(
            candle_frame, window1, window2, window3
        )

    def apply_strategy(self):
        # Generate Ultimate Oscillator signals
        signal_df = self.ultimate_oscillator_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["Ultimate_Osc_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["Ultimate_Osc_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class WilliamsRStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        lbp: int = 14,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.williams_r_signal = signals.WilliamsRSignal(candle_frame, lbp)

    def apply_strategy(self):
        # Generate Williams %R signals
        signal_df = self.williams_r_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["WilliamsR_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["WilliamsR_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class AwesomeOscillatorStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window1: int = 5,
        window2: int = 34,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.awesome_oscillator_signal = signals.AwesomeOscillatorSignal(
            candle_frame, window1, window2
        )

    def apply_strategy(self):
        # Generate Awesome Oscillator signals
        signal_df = self.awesome_oscillator_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["Awesome_Osc_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["Awesome_Osc_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class ADXStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 14,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.adx_signal = signals.ADXSignal(candle_frame, window)

    def apply_strategy(self):
        # Generate ADX signals
        signal_df = self.adx_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["ADX_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["ADX_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class AroonStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 25,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.aroon_signal = signals.AroonSignal(candle_frame, window)

    def apply_strategy(self):
        # Generate Aroon signals
        signal_df = self.aroon_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["Aroon_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["Aroon_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class CCIStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 20,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.cci_signal = signals.CCISignal(candle_frame, window)

    def apply_strategy(self):
        # Generate CCI signals
        signal_df = self.cci_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["CCI_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["CCI_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class BollingerBandsStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 20,
        window_dev: int = 2,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.bollinger_signal = signals.BollingerBandsSignal(
            candle_frame, window, window_dev
        )

    def apply_strategy(self):
        # Generate Bollinger Bands signals
        signal_df = self.bollinger_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["BB_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["BB_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class KeltnerChannelStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 20,
        window_atr: int = 10,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.keltner_signal = signals.KeltnerChannelSignal(
            candle_frame, window, window_atr
        )

    def apply_strategy(self):
        # Generate Keltner Channel signals
        signal_df = self.keltner_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["KC_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["KC_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class DonchianChannelStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 20,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.donchian_signal = signals.DonchianChannelSignal(candle_frame, window)

    def apply_strategy(self):
        # Generate Donchian Channel signals
        signal_df = self.donchian_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["Donchian_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["Donchian_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class ATRStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 14,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.atr_signal = signals.ATRSignal(candle_frame, window)

    def apply_strategy(self):
        # Generate ATR signals
        signal_df = self.atr_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["ATR_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["ATR_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class OBVStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.obv_signal = signals.OBVSignal(candle_frame)

    def apply_strategy(self):
        # Generate OBV signals
        signal_df = self.obv_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["OBV_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["OBV_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class CMFStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 20,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.cmf_signal = signals.CMFSignal(candle_frame, window)

    def apply_strategy(self):
        # Generate CMF signals
        signal_df = self.cmf_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["CMF_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["CMF_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position


class MFIStrategy(BaseStrategy):
    def __init__(
        self,
        candle_frame: CandleFrame,
        initial_balance: float,
        window: int = 14,
        allow_short: bool = False,
    ):
        super().__init__(candle_frame, initial_balance, allow_short)
        self.mfi_signal = signals.MFISignal(candle_frame, window)

    def apply_strategy(self):
        # Generate MFI signals
        signal_df = self.mfi_signal.generate_signal()

        # Apply signals to execute trades
        for index, row in signal_df.iterrows():
            if row["MFI_signal"] == 1:
                if self.short_position > 0:
                    self.sell(row["close"], row.name)  # Cover short position
                self.buy(row["close"], row.name)  # Enter long position
            elif row["MFI_signal"] == -1:
                if self.long_position > 0:
                    self.sell(row["close"], row.name)  # Exit long position
                elif self.allow_short:
                    self.sell(row["close"], row.name)  # Enter short position
