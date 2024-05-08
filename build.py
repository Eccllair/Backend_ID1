import configparser
import asyncio

from fastapi_app.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_TEST_SERVER, POSTGRES_DB
from fastapi_app.database import init_models, init_test_models, SQLALCHEMY_DATABASE_URL

asyncio.run(init_models())
asyncio.run(init_test_models())

config = configparser.ConfigParser()
config.read('alembic.ini')
config.set('alembic', 'sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

with open('alembic.ini', 'w') as configfile:
    config.write(configfile)