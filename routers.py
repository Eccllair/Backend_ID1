from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from models import User, Chat, ChatMembers
from database import get_async_session

users_router = APIRouter()
chat_router = APIRouter()

###
#  user
#  token
###
#user
@users_router.get("/")
async def get_users(session: AsyncSession = Depends(get_async_session)):
    return (await session.execute(select(User))).scalars().all()

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
    
    
#token
#TODO
# @users_router.get("/token")
# @users_router.post("/token")
# @users_router.get("/token/{id}")
# @users_router.put("/token/{id}")
# @users_router.patch("/token/{id}")
# @users_router.delete("/token/{id}")

###
#  chat
#  ChatMembers
#  Message
#  MessageRead
###

#chat
#ChatMembers
@chat_router.get("/")
async def get_chats(session: AsyncSession = Depends(get_async_session)):
    return (await session.execute(select(Chat))).scalars().all()


@chat_router.post("/")
async def create_chat(members: list[int], admins: list[int], name: str | None = None, session: AsyncSession = Depends(get_async_session)):
    group_chat = len(members) > 2
    chat = Chat(name=name, group_chat=group_chat)
    session.add(chat)
    await session.flush()
    
    for member in members:
        try:
            await session.execute(insert(ChatMembers).values(member_id=member, chat_id=chat.id, admin=member in admins))
        except IntegrityError as e:
            raise HTTPException(status_code=404, detail=f"пользователь с указанным id не найден. {e._message()}")
    
    await session.commit()
        

@chat_router.get("/{id}")
async def get_chat(id:int, session: AsyncSession = Depends(get_async_session)):
    try:
        return (await session.execute(select(Chat).where(Chat.id == id))).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"чата с id [{id}] не существует")
    
    
@chat_router.get("/{id}/members")
async def get_chat_members(id:int, session: AsyncSession = Depends(get_async_session)):
    try:
        return (await session.execute(select(ChatMembers).where(ChatMembers.chat_id == id))).scalars().all()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"чата с id [{id}] не существует")


@chat_router.put("/{id}")
async def change_chat(id:int, name: str, members: list[int], admins: list[int], session: AsyncSession = Depends(get_async_session)):
    #получение чата из бд
    try:
        chat = (await session.execute(select(Chat).where(Chat.id == id))).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"чата с id [{id}] не существует")
    
    #обновление информации о чате
    chat.name = name
    chat.group_chat = len(members) > 2
    session.add(chat)
    
    #обновление списка участников чата
    for member in members:
        member = ChatMembers(member_id=member, chat_id=chat.id, admin=member in admins)
        session.add(member)
        
    try:
        await session.commit()
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail=f"указанного пользователя не существует. {e._message()}")
    
    
@chat_router.patch("/{id}")
async def partional_change_chat(
    id:int, name: str | None = None, members: list[int] | None = None,
    admins: list[int] | None = None, session: AsyncSession = Depends(get_async_session)
):
    #получение чата из бд
    try:
        chat = (await session.execute(select(Chat).where(Chat.id == id))).scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"чата с id [{id}] не существует")
    
    #обновление списка участников чата
    if members:
        for member in members:
            memb = ChatMembers(member_id=member, chat_id=chat.id, admin=member in admins)
            session.add(memb)
    try:
        await session.flush()
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail=f"указанного пользователя не существует. {e._message()}")
    
    #обновление информации о чате
    chat_members = (await session.execute(select(ChatMembers).where(ChatMembers.chat_id == chat.id))).scalars().all()
    if name: chat.name = name
    chat.group_chat = len(chat_members) > 2
    
    await session.commit()

@chat_router.delete("/{id}")
async def delete_chat(id:int, session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(delete(Chat).where(Chat.id == id))
        await session.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail=f"чата с id [{id}] не существует")


#TODO
# @chat_router.get("/chat-members")
# @chat_router.post("/chat-members")
# @chat_router.get("/chat-members/{id}")
# @chat_router.put("/chat-members/{id}")
# @chat_router.patch("/chat-members/{id}")
# @chat_router.delete("/chat-members/{id}")


#TODO
#Message
# @chat_router.get("/messages")
# @chat_router.post("/messages")
# @chat_router.get("/messages/{id}")
# @chat_router.put("/messages/{id}")
# @chat_router.patch("/messages/{id}")
# @chat_router.delete("/messages/{id}")