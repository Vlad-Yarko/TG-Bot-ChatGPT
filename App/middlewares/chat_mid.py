from aiogram import BaseMiddleware
from typing import Dict, Any, Awaitable, Callable
from aiogram.types import TelegramObject, CallbackQuery
from App.databases.engine import main_session


class ChatID(BaseMiddleware):
    def __init__(self):
        pass

    async def __call__(self,
                        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                        event: CallbackQuery,
                        data: Dict[str, Any]
                       ):
        async with main_session() as session:
            data['chat_id'] = int(event.data.split()[-1])
            data['session'] = session
            return await handler(event, data)


