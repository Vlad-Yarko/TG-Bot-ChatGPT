from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from App.databases.requests import orm_user_start_bot, orm_create_new_chat, orm_continue_chat

from App.middlewares.db import CreateConnDB

from App.config import creator

from App.databases.requests import orm_get_all_chat_history

from App.keyboards.inline.gpt_inline import inline_chats

from App.middlewares.chat_mid import ChatID

base_command_router = Router()
base_command_router.message.filter(StateFilter(None))
base_command_router.message.middleware(CreateConnDB())
base_command_router.callback_query.filter(StateFilter(None))
base_command_router.callback_query.middleware(ChatID())


@base_command_router.message(Command('start'))
async def start_bot(message: Message, session: AsyncSession):
    await message.answer(f'Hello my dear {message.from_user.username}!')
    await orm_user_start_bot(session, message)


@base_command_router.message(Command('help'))
async def help_command(message: Message):
    await message.answer(f"""
I am your virtual assistant!
I can help you with all your questions!
I can generate photos and solve your problems, but I don't know how to open links, photos ext

My creator is {creator}
""")


@base_command_router.message(Command('new_chat'))
async def start_chat(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await state.set_state('Chat:active_chat')
    tg_id = message.from_user.id
    history = await orm_get_all_chat_history(session, tg_id)
    chat_id, current_messages = await orm_create_new_chat(session, tg_id)
    await state.update_data(history=history, messages=current_messages, chat_id=chat_id)
    await message.answer(f"Hello {message.from_user.username}, what's new?")


@base_command_router.message(Command('all_chats'))
async def all_gpt_chats_command(message: Message, session: AsyncSession):
    inline_keyboard = await inline_chats(session, message.from_user.id)
    if inline_keyboard:
        await message.answer(f"Here are our chats with you!",
                            reply_markup=inline_keyboard)
    else:
        await message.answer('No chats found')


@base_command_router.callback_query(F.data.startswith('gpt_chat'))
async def continue_chat(callback: CallbackQuery, session: AsyncSession, state: FSMContext, chat_id):
    await state.clear()
    await state.set_state('Chat:active_chat')
    tg_id = callback.message.from_user.id
    history = await orm_get_all_chat_history(session, tg_id)
    current_messages = await orm_continue_chat(session, tg_id, chat_id)
    await state.update_data(history=history, messages=current_messages, chat_id=chat_id)
    await callback.message.answer(f"Hello {callback.message.from_user.username}, what's new?")
    await callback.answer()