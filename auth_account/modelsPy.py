from pydantic import BaseModel
from typing import List
from datetime import datetime

class Interval(BaseModel):
    start_time: datetime
    end_time: datetime

class Session(BaseModel):
    type: str
    interval: Interval

class MarketSchedule(BaseModel):
    symbol: str
    sessions: List[Session]