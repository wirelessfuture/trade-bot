from abc import ABC, abstractmethod

import ta
import pandas as pd
from data_classes import CandleFrame


class BaseSignal(ABC):
    def __init__(self, candle_frame: CandleFrame) -> None:
        self.candle_frame = candle_frame
        self.df = candle_frame.to_dataframe()

    @abstractmethod
    def generate_signal(self) -> pd.DataFrame:
        pass


class RSISignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame, rsi_period: int = 14) -> None:
        super().__init__(candle_frame)
        self.rsi_period = rsi_period

    def generate_signal(self) -> pd.DataFrame:
        self.df["RSI"] = ta.momentum.RSIIndicator(
            close=self.df["close"], window=self.rsi_period
        ).rsi()
        self.df["RSI_signal"] = 0
        self.df.loc[self.df["RSI"] < 30, "RSI_signal"] = 1  # Buy signal
        self.df.loc[self.df["RSI"] > 70, "RSI_signal"] = -1  # Sell signal
        return self.df


class MACDSignal(BaseSignal):
    def __init__(
        self,
        candle_frame: CandleFrame,
        macd_fast: int = 12,
        macd_slow: int = 26,
        macd_signal: int = 9,
    ) -> None:
        super().__init__(candle_frame)
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal

    def generate_signal(self) -> pd.DataFrame:
        macd = ta.trend.MACD(
            close=self.df["close"],
            window_slow=self.macd_slow,
            window_fast=self.macd_fast,
            window_sign=self.macd_signal,
        )
        self.df["MACD"] = macd.macd()
        self.df["MACD_signal"] = macd.macd_signal()
        self.df["MACD_diff"] = macd.macd_diff()
        self.df["MACD_strategy_signal"] = 0
        self.df.loc[
            self.df["MACD"] > self.df["MACD_signal"], "MACD_strategy_signal"
        ] = 1  # Buy signal
        self.df.loc[
            self.df["MACD"] < self.df["MACD_signal"], "MACD_strategy_signal"
        ] = -1  # Sell signal
        return self.df


class StochasticSignal(BaseSignal):
    def __init__(
        self, candle_frame: CandleFrame, k_window: int = 14, d_window: int = 3
    ) -> None:
        super().__init__(candle_frame)
        self.k_window = k_window
        self.d_window = d_window

    def generate_signal(self) -> pd.DataFrame:
        stochastic = ta.momentum.StochasticOscillator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.k_window,
            smooth_window=self.d_window,
        )
        self.df["Stoch_k"] = stochastic.stoch()
        self.df["Stoch_d"] = stochastic.stoch_signal()
        self.df["Stoch_signal"] = 0
        self.df.loc[self.df["Stoch_k"] > self.df["Stoch_d"], "Stoch_signal"] = (
            1  # Buy signal
        )
        self.df.loc[
            self.df["Stoch_k"] < self.df["Stoch_d"], "Stoch_signal"
        ] = -1  # Sell signal
        return self.df


class TSISignal:
    def __init__(
        self, candle_frame: CandleFrame, window_slow: int = 25, window_fast: int = 13
    ) -> None:
        self.candle_frame = candle_frame
        self.df = candle_frame.to_dataframe()
        self.window_slow = window_slow
        self.window_fast = window_fast

    def generate_signal(self) -> pd.DataFrame:
        tsi = ta.momentum.TSIIndicator(
            close=self.df["close"],
            window_slow=self.window_slow,
            window_fast=self.window_fast,
        )
        self.df["TSI"] = tsi.tsi()
        self.df["TSI_signal"] = 0
        self.df.loc[self.df["TSI"] > 0, "TSI_signal"] = 1  # Buy signal
        self.df.loc[self.df["TSI"] < 0, "TSI_signal"] = -1  # Sell signal
        return self.df


class UltimateOscillatorSignal(BaseSignal):
    def __init__(
        self,
        candle_frame: CandleFrame,
        window1: int = 7,
        window2: int = 14,
        window3: int = 28,
    ) -> None:
        super().__init__(candle_frame)
        self.window1 = window1
        self.window2 = window2
        self.window3 = window3

    def generate_signal(self) -> pd.DataFrame:
        self.df["Ultimate_Osc"] = ta.momentum.UltimateOscillator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window1=self.window1,
            window2=self.window2,
            window3=self.window3,
        ).ultimate_oscillator()
        self.df["Ultimate_Osc_signal"] = 0
        self.df.loc[self.df["Ultimate_Osc"] > 50, "Ultimate_Osc_signal"] = (
            1  # Buy signal
        )
        self.df.loc[
            self.df["Ultimate_Osc"] < 50, "Ultimate_Osc_signal"
        ] = -1  # Sell signal
        return self.df


class WilliamsRSignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame, lbp: int = 14) -> None:
        super().__init__(candle_frame)
        self.lbp = lbp

    def generate_signal(self) -> pd.DataFrame:
        self.df["WilliamsR"] = ta.momentum.WilliamsRIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            lbp=self.lbp,
        ).williams_r()
        self.df["WilliamsR_signal"] = 0
        self.df.loc[self.df["WilliamsR"] > -20, "WilliamsR_signal"] = 1  # Buy signal
        self.df.loc[self.df["WilliamsR"] < -80, "WilliamsR_signal"] = -1  # Sell signal
        return self.df


class AwesomeOscillatorSignal(BaseSignal):
    def __init__(
        self, candle_frame: CandleFrame, window1: int = 5, window2: int = 34
    ) -> None:
        super().__init__(candle_frame)
        self.window1 = window1
        self.window2 = window2

    def generate_signal(self) -> pd.DataFrame:
        self.df["Awesome_Osc"] = ta.momentum.AwesomeOscillatorIndicator(
            high=self.df["high"],
            low=self.df["low"],
            window1=self.window1,
            window2=self.window2,
        ).awesome_oscillator()
        self.df["Awesome_Osc_signal"] = 0
        self.df.loc[self.df["Awesome_Osc"] > 0, "Awesome_Osc_signal"] = 1  # Buy signal
        self.df.loc[
            self.df["Awesome_Osc"] < 0, "Awesome_Osc_signal"
        ] = -1  # Sell signal
        return self.df


class ADXSignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame, window: int = 14) -> None:
        super().__init__(candle_frame)
        self.window = window

    def generate_signal(self) -> pd.DataFrame:
        adx = ta.trend.ADXIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
        )
        self.df["ADX"] = adx.adx()
        self.df["ADX_pos"] = adx.adx_pos()
        self.df["ADX_neg"] = adx.adx_neg()
        self.df["ADX_signal"] = 0
        self.df.loc[self.df["ADX_pos"] > self.df["ADX_neg"], "ADX_signal"] = (
            1  # Buy signal
        )
        self.df.loc[
            self.df["ADX_pos"] < self.df["ADX_neg"], "ADX_signal"
        ] = -1  # Sell signal
        return self.df


class AroonSignal:
    def __init__(self, candle_frame: CandleFrame, window: int = 25) -> None:
        self.candle_frame = candle_frame
        self.df = candle_frame.to_dataframe()
        self.window = window

    def generate_signal(self) -> pd.DataFrame:
        aroon = ta.trend.AroonIndicator(
            high=self.df["high"], low=self.df["low"], window=self.window
        )
        self.df["Aroon_Up"] = aroon.aroon_up()
        self.df["Aroon_Down"] = aroon.aroon_down()
        self.df["Aroon_signal"] = 0
        self.df.loc[self.df["Aroon_Up"] > self.df["Aroon_Down"], "Aroon_signal"] = (
            1  # Buy signal
        )
        self.df.loc[
            self.df["Aroon_Up"] < self.df["Aroon_Down"], "Aroon_signal"
        ] = -1  # Sell signal
        return self.df


class CCISignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame, window: int = 20) -> None:
        super().__init__(candle_frame)
        self.window = window

    def generate_signal(self) -> pd.DataFrame:
        self.df["CCI"] = ta.trend.CCIIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
        ).cci()
        self.df["CCI_signal"] = 0
        self.df.loc[self.df["CCI"] > 100, "CCI_signal"] = 1  # Buy signal
        self.df.loc[self.df["CCI"] < -100, "CCI_signal"] = -1  # Sell signal
        return self.df


class BollingerBandsSignal(BaseSignal):
    def __init__(
        self, candle_frame: CandleFrame, window: int = 20, window_dev: int = 2
    ) -> None:
        super().__init__(candle_frame)
        self.window = window
        self.window_dev = window_dev

    def generate_signal(self) -> pd.DataFrame:
        bollinger = ta.volatility.BollingerBands(
            close=self.df["close"], window=self.window, window_dev=self.window_dev
        )
        self.df["BB_High"] = bollinger.bollinger_hband()
        self.df["BB_Low"] = bollinger.bollinger_lband()
        self.df["BB_Mid"] = bollinger.bollinger_mavg()
        self.df["BB_signal"] = 0
        self.df.loc[
            self.df["close"] > self.df["BB_High"], "BB_signal"
        ] = -1  # Sell signal
        self.df.loc[self.df["close"] < self.df["BB_Low"], "BB_signal"] = 1  # Buy signal
        return self.df


class KeltnerChannelSignal(BaseSignal):
    def __init__(
        self, candle_frame: CandleFrame, window: int = 20, window_atr: int = 10
    ) -> None:
        super().__init__(candle_frame)
        self.window = window
        self.window_atr = window_atr

    def generate_signal(self) -> pd.DataFrame:
        keltner = ta.volatility.KeltnerChannel(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
            window_atr=self.window_atr,
        )
        self.df["KC_High"] = keltner.keltner_channel_hband()
        self.df["KC_Low"] = keltner.keltner_channel_lband()
        self.df["KC_signal"] = 0
        self.df.loc[
            self.df["close"] > self.df["KC_High"], "KC_signal"
        ] = -1  # Sell signal
        self.df.loc[self.df["close"] < self.df["KC_Low"], "KC_signal"] = 1  # Buy signal
        return self.df


class DonchianChannelSignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame, window: int = 20) -> None:
        super().__init__(candle_frame)
        self.window = window

    def generate_signal(self) -> pd.DataFrame:
        donchian = ta.volatility.DonchianChannel(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
        )
        self.df["Donchian_High"] = donchian.donchian_channel_hband()
        self.df["Donchian_Low"] = donchian.donchian_channel_lband()
        self.df["Donchian_signal"] = 0
        self.df.loc[
            self.df["close"] > self.df["Donchian_High"], "Donchian_signal"
        ] = -1  # Sell signal
        self.df.loc[self.df["close"] < self.df["Donchian_Low"], "Donchian_signal"] = (
            1  # Buy signal
        )
        return self.df


class ATRSignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame, window: int = 14) -> None:
        super().__init__(candle_frame)
        self.window = window

    def generate_signal(self) -> pd.DataFrame:
        self.df["ATR"] = ta.volatility.AverageTrueRange(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
        ).average_true_range()
        # ATR is typically used as a volatility measure, not a direct buy/sell signal, but we can still flag high volatility
        self.df["ATR_signal"] = 0
        self.df.loc[
            self.df["ATR"] > self.df["ATR"].rolling(window=self.window).mean(),
            "ATR_signal",
        ] = 1  # High volatility
        self.df.loc[
            self.df["ATR"] < self.df["ATR"].rolling(window=self.window).mean(),
            "ATR_signal",
        ] = -1  # Low volatility
        return self.df


class OBVSignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame) -> None:
        super().__init__(candle_frame)

    def generate_signal(self) -> pd.DataFrame:
        self.df["OBV"] = ta.volume.OnBalanceVolumeIndicator(
            close=self.df["close"], volume=self.df["vol"]
        ).on_balance_volume()
        self.df["OBV_signal"] = (
            self.df["OBV"].diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
        )
        return self.df


class CMFSignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame, window: int = 20) -> None:
        super().__init__(candle_frame)
        self.window = window

    def generate_signal(self) -> pd.DataFrame:
        self.df["CMF"] = ta.volume.ChaikinMoneyFlowIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            volume=self.df["vol"],
            window=self.window,
        ).chaikin_money_flow()
        self.df["CMF_signal"] = 0
        self.df.loc[self.df["CMF"] > 0, "CMF_signal"] = 1  # Buy signal
        self.df.loc[self.df["CMF"] < 0, "CMF_signal"] = -1  # Sell signal
        return self.df


class MFISignal(BaseSignal):
    def __init__(self, candle_frame: CandleFrame, window: int = 14) -> None:
        super().__init__(candle_frame)
        self.window = window

    def generate_signal(self) -> pd.DataFrame:
        self.df["MFI"] = ta.volume.MFIIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            volume=self.df["vol"],
            window=self.window,
        ).money_flow_index()
        self.df["MFI_signal"] = 0
        self.df.loc[self.df["MFI"] < 20, "MFI_signal"] = 1  # Buy signal
        self.df.loc[self.df["MFI"] > 80, "MFI_signal"] = -1  # Sell signal
        return self.df
