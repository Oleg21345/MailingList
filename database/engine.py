from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

load_dotenv()

MYSQL_PORT = os.getenv('MYSQL_PORT', '3306')

DB_URL = (
    f"mysql+aiomysql://{quote_plus(os.getenv('MYSQL_USER'))}:"
    f"{quote_plus(os.getenv('MYSQL_PASSWORD'))}@"
    f"{os.getenv('MYSQL_HOST')}/"
    f"{os.getenv('MYSQL_DB')}"
)
Base = declarative_base()

engine = create_async_engine(
    url=DB_URL,
    echo=False
)

async_sessions = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncSession:
    async with async_sessions() as session:
        yield session










