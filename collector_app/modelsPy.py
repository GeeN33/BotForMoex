from pydantic import BaseModel, Field
from typing import List
class Valute(BaseModel):
    ID: str
    NumCode: int
    CharCode: str
    Nominal: int
    Name: str
    Value: float
    VunitRate: float


class ValCurs(BaseModel):
    Date: str
    name: str
    Valute: List[Valute]

class Quote(BaseModel):
    ask: float
    last: float
    bid: float
