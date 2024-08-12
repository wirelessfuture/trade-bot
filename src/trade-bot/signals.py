from abc import ABC, abstractmethod

import ta
from pandas import DataFrame
from data_classes import KLines


class BaseSignal(ABC):
    def __init__(self, klines: KLines) -> None:
        self.klines = klines
        self.df = klines.to_dataframe()
        self.name = self.__class__.__name__

    @abstractmethod
    def generate(self) -> DataFrame:
        pass


class RSISignal(BaseSignal):
    def __init__(self, klines: KLines, rsi_period: int = 14) -> None:
        super().__init__(klines)
        self.rsi_period = rsi_period

    def generate(self) -> DataFrame:
        self.df["RSI"] = ta.momentum.RSIIndicator(
            close=self.df["close"], window=self.rsi_period
        ).rsi()
        self.df[self.name] = 0
        self.df.loc[self.df["RSI"] < 30, self.name] = 1
        self.df.loc[self.df["RSI"] > 70, self.name] = -1
        return self.df


class MACDSignal(BaseSignal):
    def __init__(
        self,
        klines: KLines,
        macd_fast: int = 12,
        macd_slow: int = 26,
        macd_signal: int = 9,
    ) -> None:
        super().__init__(klines)
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal

    def generate(self) -> DataFrame:
        macd = ta.trend.MACD(
            close=self.df["close"],
            window_slow=self.macd_slow,
            window_fast=self.macd_fast,
            window_sign=self.macd_signal,
        )
        self.df["MACD"] = macd.macd()
        self.df["MACD_signal"] = macd.macd_signal()
        self.df["MACD_diff"] = macd.macd_diff()
        self.df[self.name] = 0
        self.df.loc[self.df["MACD"] > self.df["MACD_signal"], self.name] = 1
        self.df.loc[self.df["MACD"] < self.df["MACD_signal"], self.name] = -1
        return self.df


class StochasticSignal(BaseSignal):
    def __init__(
        self, klines: KLines, k_window: int = 14, d_window: int = 3
    ) -> None:
        super().__init__(klines)
        self.k_window = k_window
        self.d_window = d_window

    def generate(self) -> DataFrame:
        stochastic = ta.momentum.StochasticOscillator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.k_window,
            smooth_window=self.d_window,
        )
        self.df["Stoch_k"] = stochastic.stoch()
        self.df["Stoch_d"] = stochastic.stoch_signal()
        self.df[self.name] = 0
        self.df.loc[self.df["Stoch_k"] > self.df["Stoch_d"], self.name] = 1
        self.df.loc[self.df["Stoch_k"] < self.df["Stoch_d"], self.name] = -1
        return self.df


class TSISignal(BaseSignal):
    def __init__(
        self, klines: KLines, window_slow: int = 25, window_fast: int = 13
    ) -> None:
        self.klines = klines
        self.df = klines.to_dataframe()
        self.window_slow = window_slow
        self.window_fast = window_fast

    def generate(self) -> DataFrame:
        tsi = ta.momentum.TSIIndicator(
            close=self.df["close"],
            window_slow=self.window_slow,
            window_fast=self.window_fast,
        )
        self.df["TSI"] = tsi.tsi()
        self.df[self.name] = 0
        self.df.loc[self.df["TSI"] > 0, self.name] = 1
        self.df.loc[self.df["TSI"] < 0, self.name] = -1
        return self.df


class UltimateOscillatorSignal(BaseSignal):
    def __init__(
        self,
        klines: KLines,
        window1: int = 7,
        window2: int = 14,
        window3: int = 28,
    ) -> None:
        super().__init__(klines)
        self.window1 = window1
        self.window2 = window2
        self.window3 = window3

    def generate(self) -> DataFrame:
        self.df["Ultimate_Osc"] = ta.momentum.UltimateOscillator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window1=self.window1,
            window2=self.window2,
            window3=self.window3,
        ).ultimate_oscillator()
        self.df[self.name] = 0
        self.df.loc[self.df["Ultimate_Osc"] > 50, self.name] = 1
        self.df.loc[self.df["Ultimate_Osc"] < 50, self.name] = -1
        return self.df


class WilliamsRSignal(BaseSignal):
    def __init__(self, klines: KLines, lbp: int = 14) -> None:
        super().__init__(klines)
        self.lbp = lbp

    def generate(self) -> DataFrame:
        self.df["WilliamsR"] = ta.momentum.WilliamsRIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            lbp=self.lbp,
        ).williams_r()
        self.df[self.name] = 0
        self.df.loc[self.df["WilliamsR"] > -20, self.name] = 1
        self.df.loc[self.df["WilliamsR"] < -80, self.name] = -1
        return self.df


class AwesomeOscillatorSignal(BaseSignal):
    def __init__(
        self, klines: KLines, window1: int = 5, window2: int = 34
    ) -> None:
        super().__init__(klines)
        self.window1 = window1
        self.window2 = window2

    def generate(self) -> DataFrame:
        self.df["Awesome_Osc"] = ta.momentum.AwesomeOscillatorIndicator(
            high=self.df["high"],
            low=self.df["low"],
            window1=self.window1,
            window2=self.window2,
        ).awesome_oscillator()
        self.df[self.name] = 0
        self.df.loc[self.df["Awesome_Osc"] > 0, self.name] = 1
        self.df.loc[self.df["Awesome_Osc"] < 0, self.name] = -1
        return self.df


class ADXSignal(BaseSignal):
    def __init__(self, klines: KLines, window: int = 14) -> None:
        super().__init__(klines)
        self.window = window

    def generate(self) -> DataFrame:
        adx = ta.trend.ADXIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
        )
        self.df["ADX"] = adx.adx()
        self.df["ADX_pos"] = adx.adx_pos()
        self.df["ADX_neg"] = adx.adx_neg()
        self.df[self.name] = 0
        self.df.loc[self.df["ADX_pos"] > self.df["ADX_neg"], self.name] = 1
        self.df.loc[self.df["ADX_pos"] < self.df["ADX_neg"], self.name] = -1
        return self.df


class AroonSignal(BaseSignal):
    def __init__(self, klines: KLines, window: int = 25) -> None:
        self.klines = klines
        self.df = klines.to_dataframe()
        self.window = window

    def generate(self) -> DataFrame:
        aroon = ta.trend.AroonIndicator(
            high=self.df["high"], low=self.df["low"], window=self.window
        )
        self.df["Aroon_Up"] = aroon.aroon_up()
        self.df["Aroon_Down"] = aroon.aroon_down()
        self.df[self.name] = 0
        self.df.loc[self.df["Aroon_Up"] > self.df["Aroon_Down"], self.name] = 1
        self.df.loc[self.df["Aroon_Up"] < self.df["Aroon_Down"], self.name] = -1
        return self.df


class CCISignal(BaseSignal):
    def __init__(self, klines: KLines, window: int = 20) -> None:
        super().__init__(klines)
        self.window = window

    def generate(self) -> DataFrame:
        self.df["CCI"] = ta.trend.CCIIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
        ).cci()
        self.df[self.name] = 0
        self.df.loc[self.df["CCI"] > 100, self.name] = 1
        self.df.loc[self.df["CCI"] < -100, self.name] = -1
        return self.df


class BollingerBandsSignal(BaseSignal):
    def __init__(
        self, klines: KLines, window: int = 20, window_dev: int = 2
    ) -> None:
        super().__init__(klines)
        self.window = window
        self.window_dev = window_dev

    def generate(self) -> DataFrame:
        bollinger = ta.volatility.BollingerBands(
            close=self.df["close"], window=self.window, window_dev=self.window_dev
        )
        self.df["BB_High"] = bollinger.bollinger_hband()
        self.df["BB_Low"] = bollinger.bollinger_lband()
        self.df["BB_Mid"] = bollinger.bollinger_mavg()
        self.df[self.name] = 0
        self.df.loc[self.df["close"] > self.df["BB_High"], self.name] = -1
        self.df.loc[self.df["close"] < self.df["BB_Low"], self.name] = 1
        return self.df


class KeltnerChannelSignal(BaseSignal):
    def __init__(
        self, klines: KLines, window: int = 20, window_atr: int = 10
    ) -> None:
        super().__init__(klines)
        self.window = window
        self.window_atr = window_atr

    def generate(self) -> DataFrame:
        keltner = ta.volatility.KeltnerChannel(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
            window_atr=self.window_atr,
        )
        self.df["KC_High"] = keltner.keltner_channel_hband()
        self.df["KC_Low"] = keltner.keltner_channel_lband()
        self.df[self.name] = 0
        self.df.loc[self.df["close"] > self.df["KC_High"], self.name] = -1
        self.df.loc[self.df["close"] < self.df["KC_Low"], self.name] = 1
        return self.df


class DonchianChannelSignal(BaseSignal):
    def __init__(self, klines: KLines, window: int = 20) -> None:
        super().__init__(klines)
        self.window = window

    def generate(self) -> DataFrame:
        donchian = ta.volatility.DonchianChannel(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
        )
        self.df["Donchian_High"] = donchian.donchian_channel_hband()
        self.df["Donchian_Low"] = donchian.donchian_channel_lband()
        self.df[self.name] = 0
        self.df.loc[self.df["close"] > self.df["Donchian_High"], self.name] = -1
        self.df.loc[self.df["close"] < self.df["Donchian_Low"], self.name] = 1
        return self.df


class ATRSignal(BaseSignal):
    def __init__(self, klines: KLines, window: int = 14) -> None:
        super().__init__(klines)
        self.window = window

    def generate(self) -> DataFrame:
        self.df["ATR"] = ta.volatility.AverageTrueRange(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            window=self.window,
        ).average_true_range()
        # ATR is typically used as a volatility measure, not a direct buy/sell signal, but we can still flag high volatility
        self.df[self.name] = 0
        self.df.loc[
            self.df["ATR"] > self.df["ATR"].rolling(window=self.window).mean(),
            self.name,
        ] = 1  # High volatility
        self.df.loc[
            self.df["ATR"] < self.df["ATR"].rolling(window=self.window).mean(),
            self.name,
        ] = -1  # Low volatility
        return self.df


class OBVSignal(BaseSignal):
    def __init__(self, klines: KLines) -> None:
        super().__init__(klines)

    def generate(self) -> DataFrame:
        self.df["OBV"] = ta.volume.OnBalanceVolumeIndicator(
            close=self.df["close"], volume=self.df["quote_asset_volume"]
        ).on_balance_volume()
        self.df[self.name] = (
            self.df["OBV"].diff().apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
        )
        return self.df


class CMFSignal(BaseSignal):
    def __init__(self, klines: KLines, window: int = 20) -> None:
        super().__init__(klines)
        self.window = window

    def generate(self) -> DataFrame:
        self.df["CMF"] = ta.volume.ChaikinMoneyFlowIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            volume=self.df["quote_asset_volume"],
            window=self.window,
        ).chaikin_money_flow()
        self.df[self.name] = 0
        self.df.loc[self.df["CMF"] > 0, self.name] = 1
        self.df.loc[self.df["CMF"] < 0, self.name] = -1
        return self.df


class MFISignal(BaseSignal):
    def __init__(self, klines: KLines, window: int = 14) -> None:
        super().__init__(klines)
        self.window = window

    def generate(self) -> DataFrame:
        self.df["MFI"] = ta.volume.MFIIndicator(
            high=self.df["high"],
            low=self.df["low"],
            close=self.df["close"],
            volume=self.df["quote_asset_volume"],
            window=self.window,
        ).money_flow_index()
        self.df[self.name] = 0
        self.df.loc[self.df["MFI"] < 20, self.name] = 1
        self.df.loc[self.df["MFI"] > 80, self.name] = -1
        return self.df
