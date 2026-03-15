import asyncio

from .session import engine
from .base import Base
from .models import * 

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 


async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all) 


if __name__=="__main__":
    # asyncio.run(init_db())
    asyncio.run(reset_db())