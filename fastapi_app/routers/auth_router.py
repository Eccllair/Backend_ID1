from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..models import User
from ..database import get_sqlite_session

auth_router = APIRouter()
templates = Jinja2Templates(directory="./fastapi_app/templates")

@auth_router.post("/sign_up")
def sign_up(login:str, password : str, name: str, birthday: date, height: int,  session: Session = Depends(get_sqlite_session)):
    try:
        user = User(login=login, pwd=password, name=name, birthday=birthday, height=height)
        session.add(user)
        session.flush()
        data={
            "id" : user.id,
            "login" : login,
            "name" : name,
            "birthday" : birthday,
            "height" : height
        }
        session.commit()
        return JSONResponse(status_code=201, content=jsonable_encoder(data), media_type="application/json")
    except IntegrityError as e:
        raise HTTPException(status_code=409, detail=f"пользователь с указанными данными уже существует. {e._message()}")
    
@auth_router.post("/sign_in", response_class=HTMLResponse)
def sign_in(request: Request, login:str, password : str, session: Session = Depends(get_sqlite_session)):
    try:
        user = session.execute(select(User).where(User.login == login)).scalar_one()
        if user.pwd == password:
            return templates.TemplateResponse(
                request=request, name="after-auth.html", context={"login": login, "age": int(abs(user.birthday-date.today()).days/365), "height": user.height}
            )
        else: raise HTTPException(status_code=403, detail=f"неверный пароль")
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=f"пользователя с логином [{login}] не существует. {e._message()}")