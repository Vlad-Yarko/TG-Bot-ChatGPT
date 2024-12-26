from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from App.databases.requests import orm_user_start_bot

from App.middlewares.db import CreateConnDB

base_command_router = Router()
base_command_router.message.filter(StateFilter(None))
base_command_router.message.middleware(CreateConnDB())


@base_command_router.message(Command('start'))
async def start_bot(message: Message, session: AsyncSession):
    await message.answer(f'Hello my dear {message.from_user.username}!')
    await orm_user_start_bot(session, message)


@base_command_router.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Help')


