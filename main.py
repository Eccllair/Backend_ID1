from fastapi import FastAPI
from routers import users_router

app = FastAPI()

app.include_router(
    router=users_router,
    prefix="/users"
)