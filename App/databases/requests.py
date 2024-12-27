from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert, and_
from App.databases.models import User, ChatHistory, ChatsHistory
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
    if not all_messages:
        all_messages = ""
    n_messages = '_._' + '_._'.join(dumps(message, ensure_ascii=False) for message in new_messages)
    messages = all_messages + n_messages
    await session.execute(update(ChatHistory)
                          .where(ChatHistory.tg_id == tg_id)
                          .values(messages=messages))
    await session.commit()


async def orm_create_new_chat(session: AsyncSession, tg_id: int):
    await session.execute(insert(ChatsHistory).values(tg_id=tg_id))
    await session.commit()
    data = await session.execute(select(ChatsHistory.chat_id, ChatsHistory.messages).where(ChatsHistory.tg_id == tg_id))
    res = data.all()
    current_chat_id, current_messages = res[-1]
    if current_messages:
        messages = [literal_eval(message) for message in current_messages[3:].split('_._')]
    else:
        messages = list()
    return current_chat_id, messages


async def orm_update_current_chat_history(session: AsyncSession, gpt_chat_id, *new_messages):
    data = await session.execute(select(ChatsHistory.messages).where(ChatsHistory.chat_id == gpt_chat_id))
    all_messages = data.scalar()
    n_messages = '_._' + '_._'.join(dumps(message, ensure_ascii=False) for message in new_messages)
    messages = all_messages + n_messages
    await session.execute(update(ChatsHistory)
                          .where(ChatsHistory.chat_id == gpt_chat_id)
                          .values(messages=messages))
    await session.commit()


async def orm_get_all_chats_one_user(session: AsyncSession, tg_id: int):
    data = await session.execute(select(ChatsHistory).where(ChatsHistory.tg_id == tg_id))
    return data.scalars().all()


async def orm_continue_chat(session: AsyncSession, tg_id: int, chat_id: int):
    data = await session.execute(select(ChatsHistory.messages)
                                 .where(and_(ChatsHistory.tg_id == tg_id,
                                             ChatsHistory.chat_id == chat_id)))
    res = data.scalar()
    if not res:
        res = list()
    return res