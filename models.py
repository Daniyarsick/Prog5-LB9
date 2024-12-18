from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    spending: float

class BonusLevel(BaseModel):
    level: str
    min_spending: float
    cashback: float