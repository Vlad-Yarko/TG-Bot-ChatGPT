from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from App.databases.models import User, ChatHistory
from aiogram.types import Message
from json import loads, dumps
from ast import literal_eval


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
        session.add(ChatHistory(
            tg_id=tg_id
        ))
        await session.commit()


async def orm_get_all_chat_history(session: AsyncSession, tg_id: int):
    data = await session.execute(select(ChatHistory.messages).where(ChatHistory.tg_id == tg_id))
    res = data.scalar()
    if res:
        messages = [literal_eval(message) for message in res[3:].split('_._')]
    else:
        messages = list()
    return messages


async def orm_update_all_chat_history(session: AsyncSession, tg_id: int, *new_messages):
    data = await session.execute(select(ChatHistory.messages).where(ChatHistory.tg_id == tg_id))
    all_messages = data.scalar()
    n_messages = '_._' + '_._'.join(dumps(message, ensure_ascii=False) for message in new_messages)
    messages = all_messages + n_messages
    await session.execute(update(ChatHistory)
                          .where(ChatHistory.tg_id == tg_id)
                          .values(messages=messages))
    await session.commit()
