from coloredlogs import install
from logging import getLogger, basicConfig, Logger


logger: Logger = getLogger("TradeBot")
FORMAT: str = "[%(asctime)-15s][%(funcName)s:%(lineno)d] %(message)s"
basicConfig(format=FORMAT)
install(level="INFO")