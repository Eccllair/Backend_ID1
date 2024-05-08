from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from ..models import User
from ..database import get_async_session

users_router = APIRouter()

@users_router.get("/")
async def get_users(login:str | None = None, session: AsyncSession = Depends(get_async_session)):
    if login: 
        try:
            return (await session.execute(select(User).where(User.login == login))).scalar_one()
        except NoResultFound:
            raise HTTPException(status_code=404, detail=f"пользоватлея с логином [{login}] не существует")
    else: return (await session.execute(select(User))).scalars().all()

@users_router.get("/{id}")
async def get_user(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        return (await session.execute(select(User).where(User.id==id))).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"пользоватлея с id [{id}] не существует")

@users_router.post("/")
async def create_user(
        name: str, surname: str, patronymic: str, mail: str,
        login: str, pwd: str, session: AsyncSession = Depends(get_async_session)
    ):
    try:
        await session.execute(
            insert(User).values(
                name=name, surname=surname, patronymic=patronymic,
                mail=mail, login=login, pwd=pwd
            )
        )
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=f"пользователь с указанными данными уже существует. {e._message()}")
    await session.commit()


@users_router.put("/{id}")
async def change_user(
        id:int, name: str, surname: str, patronymic: str, mail: str,
        login: str, pwd: str, verified: bool, session: AsyncSession = Depends(get_async_session)
    ):
    try:
        await session.execute(
            update(User).where(User.id==id).values(
                name=name, surname=surname, patronymic=patronymic,
                mail=mail, login=login, pwd=pwd, verified=verified
            )
        )
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"пользоватлея с id [{id}] не существует")
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=f"пользователь с введёнными данными уже существует {e._message()}")
    await session.commit()
    

@users_router.patch("/{id}")
async def partional_change_user(
        id: int, name: str | None = None, surname: str | None = None,
        patronymic: str | None = None, mail: str | None = None,
        verified: bool | None = None, login: str | None = None,
        pwd: str | None = None, session: AsyncSession = Depends(get_async_session)
    ):
    
    #получение записи пользователя из бд
    try:
        user = (await session.execute(select(User).where(User.id == id))).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"пользоватлея с id [{id}] не существует")
    
    #обновление информации о пользователе
    if name: user.name = name
    if surname: user.surname = surname
    if patronymic: user.patronymic=patronymic
    if mail: user.mail = mail
    if verified: user.verified = verified
    if login: user.login = login
    if pwd: user.pwd = pwd
    
    #фиксация изменений
    try:
        session.add(user)
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=f"пользователь с указанными данными уже существует. {e._message()}")


@users_router.delete("/{id}")
async def delete_user(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(delete(User).where(User.id==id))
        await session.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"пользоватлея с id [{id}] не существует")
