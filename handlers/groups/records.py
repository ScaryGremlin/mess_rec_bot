from aiogram import types

from loader import dispatcher


@dispatcher.message_handler(commands='records')
async def bot_stat(message: types.Message):
    await message.answer('Вы запросили статистику')
