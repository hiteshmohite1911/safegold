from pydantic import BaseModel
from typing import List
from datetime import datetime


class User_schema(BaseModel):
    name: str
    email: str
    created_at: datetime


class Transaction_schema(BaseModel):
    user_id: int
    amount: float
    timestamp: datetime
    type: str


class DataIngest(BaseModel):
    users: List[User_schema] = []
    transactions: List[Transaction_schema] = []
