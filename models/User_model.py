from sqlalchemy import Column, String, Integer, func, DateTime, ForeignKey
from config.database import Base


class Roles(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=True, index=True)
    email = Column(String(250), nullable=False, index=True, unique=True)
    password = Column(String(200), nullable=True)
    role = Column(Integer, ForeignKey("roles.id"), default=2)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
