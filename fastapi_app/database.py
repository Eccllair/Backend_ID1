from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from .config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_SERVER, POSTGRES_DB, POSTGRES_PORT, POSTGRES_TEST_SERVER,POSTGRES_TEST_PORT
from .models import Base

SQLALCHEMY_DATABASE_URL=f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
SQLALCHEMY_TEST_DATABASE_URL=f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_TEST_SERVER}:{POSTGRES_TEST_PORT}/{POSTGRES_DB}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
test_engine = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def init_test_models():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
async def drop_test_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async_session_maker: sessionmaker[Session] = sessionmaker(engine, class_=AsyncSession, expire_on_commit=True)
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async_test_session_maker: sessionmaker[Session] = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=True)
async def get_async_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_test_session_maker() as session:
        yield session