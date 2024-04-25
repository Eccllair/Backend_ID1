from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_DB, POSTGRES_TEST_SERVER

from models.user_model import Base as user_base

SQLALCHEMY_DATABASE_URL=f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:5444/{POSTGRES_DB}'
SQLALCHEMY_TEST_DATABASE_URL=f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_TEST_SERVER}:5440/{POSTGRES_DB}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
test_engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)

async def init_user_models():
    async with engine.begin() as conn:
        await conn.run_sync(user_base.metadata.drop_all)
        await conn.run_sync(user_base.metadata.create_all)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async_test_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=True)
async def get_async_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session