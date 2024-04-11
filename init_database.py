from models.user_model import Base as user_base
from database import engine

user_base.metadata.create_all(engine)