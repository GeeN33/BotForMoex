from typing import Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import date


class OptionBrief(BaseModel):
    model_config = ConfigDict(extra="ignore")
    delta: Optional[float] = None
    gamma: Optional[float] = None
    vega: Optional[float] = None
    theta: Optional[float] = None
    rho: Optional[float] = None
    secid: str = Field(..., max_length=12)
    days_until_expiring: Optional[int] = None
    underlying_price: Optional[float] = None
    volatility: Optional[float] = None
    underlying_asset: Optional[str] = Field(None, max_length=36)
    underlying_type: Optional[Literal['commodity', 'currency', 'futures', 'index', 'share']] = None
    theorprice: Optional[float] = None
    fee: Optional[float] = None
    expiring_date: Optional[date] = None
    lastprice: Optional[float] = None
    settleprice: Optional[float] = None