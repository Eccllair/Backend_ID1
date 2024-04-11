from typing import Optional
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[int] = mapped_column(type_=Integer(), primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(type_=String(30), unique=True, nullable=False)