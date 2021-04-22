import emoji
from aiogram import types
from aiogram.dispatcher.filters import Command

from data import config
from loader import database
from loader import dispatcher


@dispatcher.message_handler(Command('init'))
async def bot_init(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    if message.from_user.id in config.bot_admins:
        if not await database.exists_schema(schema_name):
            await database.create_schema(schema_name)
            await database.create_table_dict_problems(schema_name)
            await database.create_table_struct_messages(schema_name)
            await database.create_table_unstruct_messages(schema_name)
            await database.create_table_dict_operators(schema_name)
            await database.create_table_service_messages(schema_name)
            answer = await message.answer(emoji.emojize(':check mark: ') +
                                          'Таблицы базы данных созданы, запись журнала начата...')
        else:
            answer = await message.answer(emoji.emojize(':information: ') +
                                          'Для этого чата журнал уже пишется!')
    else:
        answer = await message.answer(emoji.emojize(':warning: ') +
                                      'Извините, но вы не админ!')
    if await database.exists_schema(schema_name):
        await database.add_service_message(schema_name, message.message_id)
        await database.add_service_message(schema_name, answer.message_id)
