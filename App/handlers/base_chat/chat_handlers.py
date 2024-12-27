from aiogram import Router, F
from aiogram.types import Message
from App.middlewares.db import CreateConnDB
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from App.config import client, gpt_model, gpt_model_image
from App.databases.requests import orm_get_all_chat_history, orm_update_all_chat_history


chat_router = Router()
chat_router.message.middleware(CreateConnDB())
chat_router.message.filter(StateFilter('Chat:active_chat'))

chat_router_image = Router()
chat_router_image.message.middleware(CreateConnDB())


@chat_router.message(Command('quit'))
async def quit_chat(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()
    await message.answer('You quit chat')


@chat_router.message(Command('generate'))
async def text_for_generate(message: Message, state: FSMContext):
    await message.delete()
    await state.set_state('Chat:generate_image')
    await message.answer("Send me, what kind of photo would you like?"
                         "Or use /return to return to usual chat")


@chat_router_image.message(Command('return'), StateFilter('Chat:generate_image'))
async def return_to_text_chat(message: Message, state: FSMContext):
    await state.set_state('Chat:active_chat')
    await message.delete()


@chat_router.message(F.text)
async def text_message_gpt(message: Message, state: FSMContext, session: AsyncSession):
    user_question = {"role": "user", "content": message.text}
    tg_id = message.from_user.id
    data = await state.get_data()
    current_messages = data['messages']
    current_messages.append(user_question)
    response = await client.chat.completions.create(
        model=gpt_model,
        messages=current_messages,
        temperature=0.7
    )
    gpt_response = response.choices[0].message.content
    gpt_response_dict = {"role": "system", "content": gpt_response}
    current_messages.append(gpt_response_dict)
    await state.update_data(messages=current_messages)
    await orm_update_all_chat_history(session, tg_id, user_question, gpt_response_dict)
    await message.answer(gpt_response)


@chat_router_image.message(F.text, StateFilter('Chat:generate_image'))
async def generate_image(message: Message, state: FSMContext, session: AsyncSession):
    user_question = message.text
    user_question_dict = {"role": "user", "content": user_question}
    tg_id = message.from_user.id
    response = await client.images.generate(
        prompt=user_question,
        model=gpt_model_image,
        response_format="url"
    )
    image_url = response.data[0].url
    gpt_response_dict = {"role": "system", "content": image_url}
    data = await state.get_data()
    current_messages = data['messages']
    current_messages.append(user_question_dict)
    current_messages.append(gpt_response_dict)
    await state.update_data(messages=current_messages)
    await orm_update_all_chat_history(session, tg_id, user_question_dict, gpt_response_dict)
    await message.answer(f"""{image_url}
""")
    await message.answer('More? or /return')

