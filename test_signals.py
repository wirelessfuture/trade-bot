from datetime import datetime, timedelta
from typing import Dict, Any
import random

import pytest
from data_classes import CandleFrame
from signals import RSISignal, MACDSignal, BollingerBandsSignal, ADXSignal


@pytest.fixture
def generate_test_data():
    def _generate_test_data(num_candles: int) -> Dict[str, Any]:
        data = {"returnData": {"digits": 5, "rateInfos": []}}

        base_open = 110000  # Starting open price in base currency * 10^digits
        base_time = datetime(2024, 8, 10, 0, 0, 0)  # Starting time

        for i in range(num_candles):
            open_price = base_open + random.randint(-100, 100)
            high_price = open_price + random.randint(0, 100)
            low_price = open_price - random.randint(0, 100)
            close_price = open_price + random.randint(-100, 100)
            volume = random.randint(1000, 2000)
            time = base_time + timedelta(minutes=i)
            time_str = time.strftime("%Y-%m-%dT%H:%M:%S")

            candle = {
                "open": open_price,
                "close": close_price - open_price,  # shift from open
                "high": high_price - open_price,  # shift from open
                "low": low_price - open_price,  # shift from open
                "ctm": time,
                "ctmString": time_str,
                "vol": volume,
            }

            data["returnData"]["rateInfos"].append(candle)

        return data

    return _generate_test_data


@pytest.fixture
def test_data(generate_test_data):
    return generate_test_data(50)


def test_rsi_signal(test_data):
    candle_frame = CandleFrame(test_data)
    rsi_signal = RSISignal(candle_frame, rsi_period=14)
    df = rsi_signal.generate_signal()

    assert "RSI" in df.columns
    assert "RSI_signal" in df.columns
    assert df["RSI"].notnull().all()
    assert df["RSI_signal"].notnull().all()


def test_macd_signal(test_data):
    candle_frame = CandleFrame(test_data)
    macd_signal = MACDSignal(candle_frame, macd_fast=12, macd_slow=26, macd_signal=9)
    df = macd_signal.generate_signal()

    assert "MACD" in df.columns
    assert "MACD_signal" in df.columns
    assert "MACD_diff" in df.columns
    assert "MACD_strategy_signal" in df.columns
    assert df["MACD"].notnull().all()
    assert df["MACD_signal"].notnull().all()
    assert df["MACD_diff"].notnull().all()
    assert df["MACD_strategy_signal"].notnull().all()


def test_bollinger_bands_signal(test_data):
    candle_frame = CandleFrame(test_data)
    bollinger_signal = BollingerBandsSignal(candle_frame, window=20, window_dev=2)
    df = bollinger_signal.generate_signal()

    assert "BB_High" in df.columns
    assert "BB_Low" in df.columns
    assert "BB_Mid" in df.columns
    assert "BB_signal" in df.columns
    assert df["BB_High"].notnull().all()
    assert df["BB_Low"].notnull().all()
    assert df["BB_Mid"].notnull().all()
    assert df["BB_signal"].notnull().all()


def test_adx_signal(test_data):
    candle_frame = CandleFrame(test_data)
    adx_signal = ADXSignal(candle_frame, window=14)
    df = adx_signal.generate_signal()

    assert "ADX" in df.columns
    assert "ADX_pos" in df.columns
    assert "ADX_neg" in df.columns
    assert "ADX_signal" in df.columns
    assert df["ADX"].notnull().all()
    assert df["ADX_pos"].notnull().all()
    assert df["ADX_neg"].notnull().all()
    assert df["ADX_signal"].notnull().all()
