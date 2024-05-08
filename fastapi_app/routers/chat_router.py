from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError

from ..models import Chat, ChatMembers
from ..database import get_async_session

chat_router = APIRouter()

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