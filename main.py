import os
import time
import json

from xtb_api_connector import APIClient
from xtb_api_commands import LoginCommand, GetChartRangeRequestCommand, GetSymbol
from data_classes import CandleFrame
from enums import Period


if __name__ == "__main__":
    assert os.getenv("XTB_USER"), "Required env variable 'XTB_USER' not found."
    assert os.getenv("XTB_PASSWORD"), "Required env variable 'XTB_PASSWORD' not found."

    client = APIClient()
    new_login = LoginCommand(
        arguments={
            "userId": os.getenv("XTB_USER"),
            "password": os.getenv("XTB_PASSWORD"),
        },
        client=client,
    )

    _ = new_login.execute()

    symbol = "BITCOIN"
    period = Period.PERIOD_M15.value
    start = int((time.time() - Period.PERIOD_M15.value*60) * 1000)
    end = int((time.time()) * 1000)

    new_get_symbol = GetSymbol({"symbol": symbol}, client=client)
    symbol_data = new_get_symbol.execute()
    print(json.dumps(symbol_data, indent=4))

    new_chart_range_request = GetChartRangeRequestCommand(
        arguments={
            "info": {
                "symbol": symbol,
                "period": period,
                "start": start,
                "end": end
            }
        },
        client=client,
    )

    candle_frame = CandleFrame(data=new_chart_range_request.execute())

    print(candle_frame.to_dataframe())

    client.disconnect()
