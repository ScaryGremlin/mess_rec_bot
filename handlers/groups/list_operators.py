import emoji
from aiogram import types
from aiogram.dispatcher.filters import Command

from data import config
from loader import database
from loader import dispatcher


@dispatcher.message_handler(Command('list_operators'))
async def list_operators(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    if await database.exists_schema(schema_name):
        message_report = ''
        list_of_dicts_operators = await database.get_list_operators(schema_name)
        for operator in list_of_dicts_operators:
            member_chat_info = await message.chat.get_member(operator['operator_id'])
            message_report = message_report + f'{member_chat_info.user.id} — {member_chat_info.user.username} \n'
        if message_report:
            answer = await message.answer(message_report)
        else:
            answer = await message.answer(emoji.emojize(':warning: ') +
                                          'В этом чате нет операторов!')
        await database.add_service_message(schema_name, message.message_id)
        await database.add_service_message(schema_name, answer.message_id)
    else:
        await message.answer(emoji.emojize(':warning: ') +
                             'Пожалуйста, начните сначала запись журнала для этого чата, '
                             'чтобы создать необходимые таблицы в базе данных!')
