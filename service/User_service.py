from fastapi.exceptions import HTTPException
from sqlalchemy import select, and_
from models.User_model import User
from service.common_service import verify_password


# get user data based on filter
def get_user_data(db, model, filters=None):

    if not filters:
        stmt = select(model)
    else:
        stmt = select(model).where(and_(*filters))

    data = db.execute(stmt).all()
    data = [dict(d._mapping)["User"] for d in data]
    return data


# authenticate user based on username and password
def authenticate_user(db, username, password):

    user = select(User.email, User.name, User.id, User.role, User.password).where(
        User.email == username
    )
    user = db.execute(user).fetchone()._asdict()

    if not user:
        raise HTTPException(400, "User not found")

    if not verify_password(password, user["password"]):
        raise HTTPException(400, "Invalid credentials")
    user.pop("password")
    return user
