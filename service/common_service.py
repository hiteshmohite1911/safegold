import jwt
from config.settings import get_settings
from sqlalchemy import delete
from datetime import datetime, timedelta
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


# create jwt token
def generate_jwt(user):
    try:
        user["exp"] = datetime.now() + timedelta(minutes=1000)
        return jwt.encode(user, key=settings.SECRET_KEY)
    except Exception as e:
        print(e)


# password hashing
def hashed_password(password):
    return pwd_context.hash(password)


# password verification
def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


# common insert method to repeat insert code
async def insert(db, model, data, bulk=False):
    try:
        if bulk == False:
            obj = model(**data)
            db.add(obj)
            db.commit()
            return True
        else:
            data_set = [model(**dict(d)) for d in data]
            db.add_all(data_set)
            db.commit()
            return True
    except Exception as e:
        print("\n", e, "\n")
        return False


# delete any data by id column
def delete_by_id(db, model, id):
    try:
        resp = delete(model).where(model.id == id)
        db.execute(resp)
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False


# Response format
def Response(status=200, message="", data=None, error=None):
    return {"status": status, "message": message, "data": data, "error": error}
