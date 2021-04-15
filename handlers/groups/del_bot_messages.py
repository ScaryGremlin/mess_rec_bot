from aiogram import types
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.filters import Regexp
from aiogram.dispatcher.filters import Command

from data import config
from loader import database
from loader import dispatcher
from loader import bot


@dispatcher.message_handler(Command('delete'))
async def del_message(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    dict_del_messages = await database.get_messages_for_delete(schema_name)
    for d in dict_del_messages:
        print(d['message_id'])
        await bot.delete_message(message.chat.id, d['message_id'])
