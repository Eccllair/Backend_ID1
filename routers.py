from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete

from models.user_model import User
from database import get_async_session

users_router = APIRouter()

@users_router.get("/")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return (await session.execute(select(User))).scalars().all()

@users_router.post("/")
async def create_user(name: str, session: AsyncSession = Depends(get_async_session)):
    await session.execute(insert(User).values(name=name))
    await session.commit()

@users_router.put("/{id}")
async def change_user(id: int, name: str, session: AsyncSession = Depends(get_async_session)):
    await session.execute(update(User).where(User.id==id).values(name=name))
    await session.commit()

@users_router.delete("/{id}")
async def delete_user(id: int, session: AsyncSession = Depends(get_async_session)):
    await session.execute(delete(User).where(User.id==id))
    await session.commit()
