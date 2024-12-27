from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession
from App.databases.requests import orm_get_all_chats_one_user
from ast import literal_eval


async def inline_chats(session: AsyncSession, tg_id: int):
    keyboard = list()
    for chat in await orm_get_all_chats_one_user(session, tg_id):
        try:
            first_message = literal_eval(chat.messages[3:].split('_._')[0])
            first_question = first_message['content']
        except (IndexError, TypeError, SyntaxError):
            first_question = 'empty chat'
        button = [InlineKeyboardButton(text=first_question, callback_data=f'gpt_chat {chat.chat_id}')]
        keyboard.append(button)
    if keyboard:
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
    else:
        inline_keyboard = []
    return inline_keyboard
