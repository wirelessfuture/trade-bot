import time

from data_classes import CandleFrame
from enums import Period
from constants import XTB_USER, XTB_PASSWORD
from xtb_api_connector import APIClient
from xtb_api_commands import LoginCommand, GetChartLastRequestCommand, GetServerTime
import strategies



if __name__ == "__main__":
    client = APIClient()
    new_login = LoginCommand(
        arguments={
            "userId": XTB_USER,
            "password": XTB_PASSWORD,
        },
        client=client,
    )
    _ = new_login.execute()

    new_get_server_time = GetServerTime(None, client)
    server_time = new_get_server_time.execute()
    print(server_time.get("returnData"))

    symbols = [
        "BITCOIN",
        "ETHEREUM"
    ]

    for symbol in symbols:
        period = Period.PERIOD_M30.value
        start = int((time.time() - Period.PERIOD_MN1.value * 60) * 1000)

        new_chart_last_request = GetChartLastRequestCommand(
            arguments={
                "info": {"symbol": symbol, "period": period, "start": start}
            },
            client=client,
        )

        candle_frame = CandleFrame(data=new_chart_last_request.execute())

        initial_balance = 5000
        short = True

        obv = strategies.OBVStrategy(
            candle_frame, initial_balance=initial_balance, allow_short=short
        )
        rsi = strategies.RSIStrategy(
            candle_frame, initial_balance=initial_balance, allow_short=short
        )
        macd = strategies.MACDStrategy(
            candle_frame, initial_balance=initial_balance, allow_short=short
        )

        # Combine strategies
        combined_strategy = strategies.CombinedStrategy(
            candle_frame,
            initial_balance=initial_balance,
            strategies=[obv, rsi, macd],
            allow_short=short,
        )
        combined_strategy.apply_strategy()
        print(
            combined_strategy.__class__.__name__,
            symbol,
            f"Starting Balance: ${initial_balance}",
        )
        print(
            obv.__class__.__name__,
            rsi.__class__.__name__,
            macd.__class__.__name__,
        )
        print(combined_strategy.get_trade_log())

        time.sleep(1)

    client.disconnect()
