from fastapi import APIRouter, Depends
from config.database import get_session
from sqlalchemy.orm import Session
from service.data_generator import generate_fake_data

from schema.Dataingest_schema import DataIngest
from service.common_service import Response
from service.Transaction_service import get_transaction_data, get_summary, data_ingestor
from models.Transaction_model import Transaction
from routers.Auth import get_current_user


router = APIRouter()

# to add users data and transaction data through faker
@router.get("/generate_data")
def data_seeder(db: Session = Depends(get_session), token=Depends(get_current_user)):
    resp = generate_fake_data(db, num_users=100, num_transactions=1000)
    return resp


# load data after reading from request body, as per requirements mentioned in document
@router.post("/ingest")
async def data_ingest(
    request: DataIngest,
    db: Session = Depends(get_session),
    token=Depends(get_current_user),
):
    request = dict(request)

    response = await data_ingestor(db,request)

    return Response(data=response)


# get transaction data based on given filters data 
@router.get("/transaction")
def get_transaction(
    user_id: str = None,
    type: str = None,
    date_from: str = None,
    date_to: str = None,
    db: Session = Depends(get_session),
    token=Depends(get_current_user),
):
    filters = []
    if not token['is_admin']:
        user_id=token['id']
    if user_id:
        filters.append(Transaction.user_id == user_id)
    if type:
        filters.append(Transaction.type == type)
    if date_from:
        filters.append(Transaction.timestamp >= date_from)
    if date_to:
        filters.append(Transaction.timestamp <= date_to)

    if filter == {}:
        transaction_data = get_transaction_data(db, Transaction)
    else:
        transaction_data = get_transaction_data(db, Transaction, filters)
    return transaction_data


# transaction summary for user, if admin then summary for all data else summary for user specific data
@router.get("/transactions/summary")
def transaction_summary(
    db: Session = Depends(get_session), token=Depends(get_current_user)
):
    user_id=None
    if not token['is_admin']:
        user_id=token['id']
    summary_data = get_summary(db, user_id)
    return summary_data
