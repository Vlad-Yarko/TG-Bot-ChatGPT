from aiogram.types import BotCommand\

commands = [
    BotCommand(command='start', description='start bot'),
    BotCommand(command='help', description='help you'),
    BotCommand(command='new_chat', description='start your chat with gpt'),
    BotCommand(command='all_chats', description='see all your chats'),
    BotCommand(command='quit', description='quit current chat'),
    BotCommand(command='generate', description='generate a photo'),
    BotCommand(command='return', description='return to text chat')
]