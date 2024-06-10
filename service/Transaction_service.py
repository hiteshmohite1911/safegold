from sqlalchemy import select, or_, and_, func
from models.Transaction_model import Transaction
from models.User_model import User
from service.common_service import insert


# transaction based filters
def get_transaction_data(db, model, filters=None):

    if not filters:
        stmt = select(model).limit(100)
    else:
        stmt = select(model).where(and_(*filters)).limit(100)
    data = db.execute(stmt).all()
    data = [dict(d._mapping)["Transaction"] for d in data]
    return data


# summary data, if admin then summary for all transaction data, else only for logged in user
def get_summary(db, user_id=None):

    if user_id:
        stmt = select(
            func.count(Transaction.id).label("total_transactions"),
            func.sum(Transaction.amount).label("total_amount"),
            func.avg(Transaction.amount).label("average_amount"),
        ).where(Transaction.user_id == user_id)

    else:
        stmt = select(
            func.count(Transaction.id).label("total_transactions"),
            func.sum(Transaction.amount).label("total_amount"),
            func.avg(Transaction.amount).label("average_amount"),
        )

    data = db.execute(stmt).fetchone()._asdict()
    return data


# data ingestor as per requirement
async def data_ingestor(db, request):
    response = {
        "users": "Users data saved",
        "transactions": "Transaction data saved",
    }

    users_data = request["users"]
    transactions_data = request["transactions"]

    users_data = await insert(db, User, users_data, True)
    transactions_data = await insert(db, Transaction, transactions_data, True)

    if not users_data:
        response["users"] = "Users data not saved"
    if not transactions_data:
        response["transactions"] = "Transaction data not saved"

    return response
