from jwt import encode, decode

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from datetime import datetime, timedelta

from ..database import get_async_session
from ..models import Token, User
from ..config import (
    JWT_SECRET,
    ACCESS_TOKEN_LIFE_TIME as AT,
    REFRESH_TOKEN_LIFE_TIME as RT,
    JWT_ALG
)

async def generate(user_login: str, refresh_token: str | None = None):
    date_of_creation = datetime.now()
    if (refresh_token): date_of_expiration = date_of_creation + timedelta(days=RT)
    else: date_of_expiration = date_of_creation + timedelta(days=AT)
    
    json = {
        'login': user_login,
        'date_of_creation': str(date_of_creation),
        'date_of_expiration': str(date_of_expiration),
        "alg": JWT_ALG,
        "typ": "refresh" if refresh_token else "access"
    }
    
    
    jwt_token = encode(json, JWT_SECRET + refresh_token if refresh_token else "", algorithm=JWT_ALG)
    
    session: AsyncSession = Depends(get_async_session)
    user: User = (await session.execute(select(User).where(User.login == user_login))).scalar_one()
        
    await session.execute(
        insert(Token).values(
            refresh=bool(refresh_token), jwt=jwt_token,
            date_of_creation=date_of_creation, date_of_expiration=date_of_expiration,
            user_id=user.id
        )
    )
    
    session.commit()
    
    return jwt_token

async def encode(jwt_str: str):
    return decode(jwt_str, JWT_SECRET, algorithms=[JWT_ALG])