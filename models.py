from typing import Optional
from sqlalchemy.sql import func
from sqlalchemy import (
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)


#родительский класс таблицы
class Base(DeclarativeBase):
    pass


#пользовтель
class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(type_=Integer(), primary_key=True, autoincrement=True)      #уникальный идентификатор
    name: Mapped[str] = mapped_column(type_=String(255), unique=False, nullable=False)          #имя
    surname: Mapped[str] = mapped_column(type_=String(255), unique=False, nullable=False)       #фамилия
    patronymic: Mapped[str] = mapped_column(type_=String(255), unique=False, nullable=True)     #отчество
    mail: Mapped[str] = mapped_column(type_=String(255), unique=True, nullable=False)           #почта для верификации
    verified: Mapped[bool] = mapped_column(type_=Boolean(), default=False, nullable=False)      #почта подтверждена/не подтверждена
    login: Mapped[str] = mapped_column(type_=String(255), unique=True, nullable=False)          #уникальное имя пользователя
    pwd: Mapped[str] = mapped_column(type_=String(255), unique=False, nullable=False)           #хэш пароля


#чат
class Chat(Base):
    __tablename__ = "chat"
    
    id: Mapped[int] = mapped_column(type_=Integer(), primary_key=True, autoincrement=True)      #уникальный идентификатор
    name: Mapped[str] = mapped_column(type_=String(255), nullable=True)                        #название чата
    group_chat: Mapped[bool] = mapped_column(type_=Boolean(), default=False, nullable=False)    #групповой чат/личный чат


#участники чата
class ChatMembers(Base):
    __tablename__ = "chat_members"
    id: Mapped[int] = mapped_column(type_=Integer(), primary_key=True, autoincrement=True)      #уникальный идентификатор
    member_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))             #участник чата
    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete='CASCADE'))               #чат
    admin: Mapped[bool] = mapped_column(Boolean(), default=False)                               #администратор чата/участник чата
    
    UniqueConstraint('member_id', 'chat_id', name='clone_protection')                           #вторичный ключ, для защиты от дублирования

#сообщения
class Message(Base):
    __tablename__ = "message"
    
    id: Mapped[int] = mapped_column(type_=Integer(), primary_key=True, autoincrement=True)      #уникальный идентификатор
    text: Mapped[str] = mapped_column(type_=String())                                           #сообщение
    sender_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='SET NULL'))            #отправитель
    chat_id: Mapped[int] = mapped_column(ForeignKey(Chat.id, ondelete='CASCADE'))               #получатель


#список людей, прочитавших сообщение
class MessageRead(Base):
    __tablename__ = "message_read"
    
    id: Mapped[int] = mapped_column(type_=Integer(), primary_key=True, autoincrement=True)      #уникальный идентификатор
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))               #пользователь, прочитавший сообщение
    message_id: Mapped[int] = mapped_column(ForeignKey(Message.id, ondelete="CASCADE"))         #сообщение


#токены авторизации пользователя
class Token(Base):
    __tablename__ = "user_and_message"
    
    id: Mapped[int] = mapped_column(type_=Integer(), primary_key=True, autoincrement=True)                              #уникальный идентификатор
    refresh: Mapped[bool] = mapped_column(type_=Boolean(), nullable=False)                                              #Refresh token/Access token
    jwt: Mapped[str] = mapped_column(type_=String(), nullable=False, unique=True)                                       #собствено сам токен
    date_of_creation: Mapped[str] = mapped_column(type_=DateTime(timezone=True), default=func.now(), nullable=False)    #дата создания
    date_of_expiration: Mapped[str] = mapped_column(type_=DateTime(timezone=True), nullable=False)                      #дата истечения токена
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"), nullable=False)                                           #пользователь, которому принадлежит токен

    
    