from enum import Enum


class Period(Enum):
    PERIOD_M1 = 1  # 1 minute
    PERIOD_M5 = 5  # 5 minutes
    PERIOD_M15 = 15  # 15 minutes
    PERIOD_M30 = 30  # 30 minutes
    PERIOD_H1 = 60  # 60 minutes (1 hour)
    PERIOD_H4 = 240  # 240 minutes (4 hours)
    PERIOD_D1 = 1440  # 1440 minutes (1 day)
    PERIOD_W1 = 10080  # 10080 minutes (1 week)
    PERIOD_MN1 = 43200  # 43200 minutes (30 days)
