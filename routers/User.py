from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from config.database import get_session
from schema.User_schema import Transaction_schema
from models.Transaction_model import Transaction
from models.User_model import User
from service.Auth_service import delete_access
from service.User_service import get_user_data
from service.common_service import insert, Response, delete_by_id
from routers.Auth import get_current_user

router = APIRouter()


# add transaction api added, user to added transaction
@router.post("/add_transaction")
async def add_transaction(
    request: Transaction_schema,
    db: Session = Depends(get_session),
    token=Depends(get_current_user),
):
    request = dict(request)
    request["user_id"] = token["id"]
    transaction = await insert(db, Transaction, request)
    if not transaction:
        return Response(400, "Data not inserted")

    return Response(message="Data inserted")


# delete transaction api added, only admin user can delete
@router.post("/delete_transaction/{transaction_id}")
def delete_transaction(
    transaction_id,
    db: Session = Depends(get_session),
    access=Depends(delete_access),
):

    transaction = delete_by_id(db, Transaction, transaction_id)
    print("transaction", transaction)
    if not transaction:
        return Response(400, "Data not deleted")

    return Response(message="Data deleted")


# users data filter, if admin then can get many users else only logged in user data will be shown
@router.get("/user")
def get_user(
    name: str = None,
    email: str = None,
    db: Session = Depends(get_session),
    token=Depends(get_current_user),
):
    filters = []

    if not token["is_admin"]:
        email = token["email"]
        name = token["name"]
    if name:
        filters.append(User.name == name)
    if email:
        filters.append(User.email == email)

    if filter == {}:
        user_data = get_user_data(db, User)
    else:
        user_data = get_user_data(db, User, filters)
    return user_data
