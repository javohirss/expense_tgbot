from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings

uri = settings.DB_URI

engine = create_async_engine(uri, echo=True)

MyAsyncSession = async_sessionmaker(engine, expire_on_commit=False)