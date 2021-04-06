from aiogram import types

from loader import dispatcher


@dispatcher.message_handler(content_types='text', state=None)
async def bot_echo(message: types.Message):
    await message.answer(message.text)

