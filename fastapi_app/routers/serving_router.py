from fastapi import (
    APIRouter,
    BackgroundTasks   
)

from datetime import datetime

serving_router = APIRouter()

@serving_router.get("/get_time")
async def get_time(backgroundTasks: BackgroundTasks):
    dt = datetime.now()
    time = f"{dt.hour}:{dt.minute}:{dt.second}"
    backgroundTasks.add_task(lambda: print(time))
    return time


@serving_router.get("/check")
async def check(name: str | None = None):
    return name if name else "Параметр отсутствует"