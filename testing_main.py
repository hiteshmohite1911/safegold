from fastapi.testclient import TestClient
from app import app
from config.database import get_session
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    TIMESTAMP,
    ForeignKey,
    Float,
    DateTime,
    func,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

token={}

client = TestClient(app)

SQLITE_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLITE_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    type = Column(String(10), nullable=False)
    user_id = Column(ForeignKey("users.id"))
    timestamp = Column(TIMESTAMP, server_default=func.now())


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


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db


def test_register():
    response = client.post(
        "http://localhost:8000/register",
        json={"username": "safegold2@sg.com", "password": "safegold"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": 200,
        "message": "User registered",
        "data": None,
        "error": None,
    }


def test_login():
    response = client.post(
        "http://localhost:8000/login", data={"username": "safegold22@sg.com", "password": "safegold"}
    )
    assert response.status_code == 200
    # test_token= response.json()["access"]
    # assert response.json() == {"access": "jwt.access.token"}




def test_summary():
    response = client.get(
        "http://localhost:8000/data/transaction",
        headers={"Authorization": f"Bearer {test_token}"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "total_transactions": 13,
        "total_amount": 5595.549958229065,
        "average_amount": 430.42691986377423,
    }
