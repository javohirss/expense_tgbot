from sqlalchemy import select, insert

from database.models import User
from database.session import MyAsyncSession


class UserService:
    @classmethod
    async def get_all_users(cls):
        async with MyAsyncSession() as session:
            query = select(User)
            result = await session.execute(query)
            return result.scalars().all()
        
    
    @classmethod
    async def get_or_create_user(cls, telegram_user_id):
        async with MyAsyncSession() as session:
            query = select(User).where(User.telegram_user_id == telegram_user_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user is None:
                insert_query = insert(User).values(telegram_user_id=telegram_user_id).returning(User)
                insert_result = await session.execute(insert_query)
                user = insert_result.scalar_one()
                await session.commit()

            return user
