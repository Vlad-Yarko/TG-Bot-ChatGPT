from aiogram import Bot, Dispatcher
import asyncio
from dotenv import load_dotenv, find_dotenv
from App.cmds import commands
from App.config import TOKEN
from App.handlers.base_chat.chat_handlers import chat_router, chat_router_image
from App.handlers.base_commands import base_command_router


load_dotenv(find_dotenv())

bot = Bot(token=TOKEN)

dp = Dispatcher()
dp.include_routers(
    base_command_router,
    chat_router,
    chat_router_image
)


async def main():
    await bot.set_my_commands(commands=commands)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    print('Start')


asyncio.run(main())