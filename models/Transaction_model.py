from sqlalchemy import Column, String, Integer, DateTime, func, Float, ForeignKey, TIMESTAMP
from config.database import Base


class Transaction(Base):
    __tablename__='transactions'
    
    id = Column(Integer, primary_key=True)
    amount=Column(Float, nullable=False)
    type = Column(String(10), nullable=False)
    user_id = Column(ForeignKey('users.id'))
    timestamp = Column(TIMESTAMP, server_default=func.now())
