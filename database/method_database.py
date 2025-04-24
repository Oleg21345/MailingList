from sqlalchemy import select
from .engine import async_sessions
from .model import Users

class MetodSQL:

    @staticmethod
    async def add(tgid, username, at):
        async with async_sessions() as session:
            user = Users(
                telegram_id=tgid,
                username=username,
                at=at
            )
            session.add(user)
            await session.commit()

    @staticmethod
    async def get_all_users():
        async with async_sessions() as session:
            query = select(Users.telegram_id, Users.at)
            result = await session.execute(query)
            rows = result.all()
            return [{"user_id": row.telegram_id, "registered_at": row.at} for row in rows]

    @staticmethod
    async def is_user_registered(tgid):
        async with async_sessions() as session:
            query = select(Users).filter(Users.telegram_id == tgid)
            result = await session.execute(query)
            user = result.scalars().first()
            return user is not None








