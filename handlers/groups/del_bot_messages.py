from aiogram import types
from aiogram.dispatcher.filters import Command

from data import config
from loader import bot
from loader import database
from loader import dispatcher


@dispatcher.message_handler(Command('delete'))
async def del_message(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    if await database.exists_schema(schema_name):
        await database.add_service_message(schema_name, message.message_id)
        dict_del_messages = await database.get_messages_for_delete(schema_name)
        for del_mess in dict_del_messages:
            await bot.delete_message(message.chat.id, del_mess['message_id'])
        await database.clear_table(schema_name, config.TABLE_SERVICE_MESSAGES)
    else:
        pass
