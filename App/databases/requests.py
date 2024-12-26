from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from App.databases.models import User
from aiogram.types import Message


async def orm_user_start_bot(session: AsyncSession, message: Message):
    tg_id = message.from_user.id
    chat_id = message.chat.id
    data = await session.execute(select(User).where(User.tg_id == tg_id))
    result = data.scalar()
    if not result:
        session.add(User(
            tg_id=tg_id,
            chat_id=chat_id
        ))
        await session.commit()
