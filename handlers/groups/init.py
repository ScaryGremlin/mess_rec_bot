from aiogram import types
from aiogram.dispatcher.filters import Command

from data import config
from loader import database
from loader import dispatcher


@dispatcher.message_handler(Command('init'))
async def bot_init(message: types.Message):
    if message.from_user.id in config.owners:
        schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
        if not await database.exists_schema(schema_name):
            await database.create_schema(schema_name)
            await database.create_table_dict_problems(schema_name=schema_name, table_name=config.DICT_PROBLEMS)
            await database.create_table_struct(schema_name=schema_name, table_name=config.MESSAGES_STRUCT)
            await database.create_table_unstruct(schema_name=schema_name, table_name=config.MESSAGES_UNSTRUCT)
            await database.create_table_admins(schema_name=schema_name, table_name=config.DICT_ADMINS)
            await database.create_table_users(schema_name=schema_name, table_name=config.DICT_USERS)
            await message.answer('Запись в базу данных инициализирована, таблицы созданы.')
        else:
            await message.answer('Инициализация для этого чата уже произведена!')
    else:
        await message.answer('Извините, но вы не администратор!')
