import asyncio

from fastapi import (
    APIRouter,
    BackgroundTasks
)
from datetime import datetime

from ..database import init_models

serving_router = APIRouter()

#TODO добавить секьюрность
@serving_router.post("/reset_database")
async def reset_database():
    await init_models()
    return 200


@serving_router.get("/get_time")
async def get_time(backgroundTasks: BackgroundTasks):
    dt = datetime.now()
    time = f"{dt.hour}:{dt.minute}:{dt.second}"
    backgroundTasks.add_task(lambda: print(time))
    return time


@serving_router.get("/check")
async def check(name: str | None = None):
    return name if name else "Параметр отсутствует"