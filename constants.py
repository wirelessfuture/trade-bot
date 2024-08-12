import os

from dotenv import load_dotenv

load_dotenv()


# Key Constants
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_TESTNET_API_KEY = os.getenv("BINANCE_TESTNET_API_KEY")
BINANCE_TESTNET_API_SECRET = os.getenv("BINANCE_TESTNET_API_SECRET")

# Currency Constants
BINANCE_TRADE_CURRENCY = "USDC"

# Endpoint Constants
BINANCE_TESTNET_BASE_URL = "https://testnet.binance.vision"
BINANCE_TESTNET_DATA_URL = "https://data-api.binance.vision"