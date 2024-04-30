from fastapi import FastAPI
from .routers import users_router, chat_router

app = FastAPI()

app.include_router(
    router=users_router,
    prefix="/users"
)

app.include_router(
    router=chat_router,
    prefix="/chats"
)