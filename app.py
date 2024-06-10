from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from config.settings import get_settings

setting = get_settings()

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers.Auth import router as AuthRouter
from routers.DataTransaction import router as DatatransactionRouter
from routers.User import router as UserRouter


app.include_router(AuthRouter,tags=['Authentication'])
app.include_router(DatatransactionRouter, prefix='/data',tags=['Data Transaction'])
app.include_router(UserRouter,tags=['User'])

@app.get('/')
def docs():
    return RedirectResponse('/docs')

