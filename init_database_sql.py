from models.user_sql import create_user_table
from database import get_async_session
from fastapi import Depends

session = Depends(get_async_session)
create_user_table(session)