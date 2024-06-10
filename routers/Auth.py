from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
import jwt

from service.common_service import generate_jwt, hashed_password, insert, Response
from config.database import get_session
from service.User_service import authenticate_user
from schema.User_schema import Login
from models.User_model import User
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from config.settings import get_settings

settings = get_settings()

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# login router
@router.post("/login")
async def login(request: Login, db: Session = Depends(get_session)):
    request = dict(request)

    user = authenticate_user(db, request["username"], request["password"])
    if not user:
        return Response(status_code=400, content="Invalid credentials")

    token = generate_jwt(user)
    return {"access": token}


# token router to make Swagger api call secure by JWT token
@router.post("/token", include_in_schema=False)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )
    token = generate_jwt(user)
    return {"access_token": token, "token_type": "bearer"}


# registering user by accepting username and password
@router.post("/register")
async def register(request: Login, db: Session = Depends(get_session)):
    request = dict(request)

    user_obj = {
        "email": request["username"],
        "password": hashed_password(request["password"]),
    }
    user = await insert(db, User, user_obj)

    if not user:
        return Response(status=400, message="Registration failed")

    return Response(200, "User registered")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if not payload:
            raise HTTPException(401, "Invalid token")
        payload["is_admin"] = True if payload["role"] == 1 else False
        return payload
    except Exception as e:
        print("error   ", e)
        raise HTTPException(401, "Invalid token")
