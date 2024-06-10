from pydantic import BaseModel

class Login(BaseModel):
    username:str
    password:str
    
    
class Transaction_schema(BaseModel):
    amount: float
    type: str
    
