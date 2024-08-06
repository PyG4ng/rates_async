import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from configs import config

load_dotenv(f'{config.ROOT_FOLDER}/.env')

# PG_DSN = f"postgresql+asyncpg://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('LOCAL_HOST')}:5432/" \
#          f"{os.getenv('PG_DB')}"

PG_DSN = f"postgresql+asyncpg://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('REMOTE_HOST')}:5432/" \
         f"{os.getenv('PG_DB')}"

engine = create_async_engine(PG_DSN)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


class TimeControl(Base):
    __tablename__ = 'time_control'
    id = Column(Integer, primary_key=True)
    what_to_do = Column(String(50))
    time_to_check = Column(Integer)
    status = Column(String(50))


async def get_time_control_status():
    async with Session() as session:
        result = await session.execute(select(TimeControl.status).where(TimeControl.id == 1))
        fetched_result = result.fetchall()
        return fetched_result[0][-1]


async def get_time_control_wtd():
    async with Session() as session:
        result = await session.execute(select(TimeControl.what_to_do).where(TimeControl.id == 1))
        fetched_result = result.fetchall()
        return fetched_result[0][-1]


async def get_time_control_time_to_check():
    async with Session() as session:
        result = await session.execute(select(TimeControl.time_to_check).where(TimeControl.id == 1))
        fetched_result = result.fetchall()
        return fetched_result[0][-1]
