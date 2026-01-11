from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class ValueModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    value: float

class BarModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    timestamp: datetime
    open: ValueModel
    high: ValueModel
    low: ValueModel
    close: ValueModel
    volume: ValueModel

class DataModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    symbol: str
    bars: List[BarModel]


class BarPair(BaseModel):
    timestamp: datetime
    close: float
    ema: Optional[float] = 0


class OptionModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    open_interest: ValueModel
    implied_volatility: ValueModel
    theoretical_price: ValueModel
    delta: ValueModel
    gamma: ValueModel
    theta: ValueModel
    vega: ValueModel
    rho: ValueModel


class QuoteModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    symbol: str
    timestamp: str
    ask: ValueModel
    ask_size: ValueModel
    bid: ValueModel
    bid_size: ValueModel
    last: ValueModel
    last_size: ValueModel
    volume: ValueModel
    turnover: ValueModel
    open: ValueModel
    high: ValueModel
    low: ValueModel
    close: ValueModel
    change: ValueModel
    option: OptionModel


class StockModel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    symbol: str
    quote: QuoteModel