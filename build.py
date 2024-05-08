import configparser

from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_TEST_SERVER, POSTGRES_DB

#TODO from . database import SQLALCHEMY_DATABASE_URL
SQLALCHEMY_DATABASE_URL=f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_TEST_SERVER}:5444/{POSTGRES_DB}'

config = configparser.ConfigParser()
config.read('alembic.ini')
config.set('alembic', 'sqlalchemy.url', SQLALCHEMY_DATABASE_URL)

with open('alembic.ini', 'w') as configfile:
    config.write(configfile)