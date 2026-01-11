from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ValueField(BaseModel):
    value: str


class Position(BaseModel):
    model_config = ConfigDict(extra="ignore")
    symbol: str
    quantity: ValueField
    maintenance_margin: ValueField
    unrealized_pnl: ValueField
    current_price: Optional[ValueField] = None  # Нужно корректно обозначить необязательные поля


class PortfolioForts(BaseModel):
    available_cash: ValueField
    money_reserved: ValueField


class Account(BaseModel):
    model_config = ConfigDict(extra="ignore")
    account_id: str
    type: str
    status: str
    equity: ValueField
    unrealized_profit: ValueField
    positions: List[Position]
    cash: List[ValueField]
    portfolio_forts: PortfolioForts
    open_account_date: str
    first_trade_date: str
    first_non_trade_date: str


class Availability(BaseModel):
    value: str
    halted_days: int

class RiskRate(BaseModel):
    value: float

class TradingAssets(BaseModel):
    model_config = ConfigDict(extra="ignore")
    symbol: str
    account_id: str
    tradeable: bool
    longable: Availability
    shortable: Availability
    long_risk_rate: RiskRate
    short_risk_rate: RiskRate
    is_tradable: bool


class Quantity(BaseModel):
    value: str


class LimitPrice(BaseModel):
    value: str


class Order(BaseModel):
    model_config = ConfigDict(extra="ignore")
    account_id: str
    symbol: str
    quantity: Quantity
    side: str
    type: str
    time_in_force: str
    limit_price: LimitPrice
    stop_condition: str
    legs: List
    client_order_id: str
    valid_before: str
    comment: str


class OrderDetail(BaseModel):
    model_config = ConfigDict(extra="ignore")
    order_id: str
    exec_id: str
    status: str
    order: Order
    transact_at: str


class Orders(BaseModel):
    orders: List[OrderDetail]