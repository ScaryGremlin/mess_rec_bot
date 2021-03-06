import re

import emoji
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.storage import FSMContext

from data import config
from loader import database
from loader import dispatcher
from states import AddOperatorsQuestions


@dispatcher.message_handler(Command('add_operators'))
async def add_operators(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    if await database.exists_schema(schema_name):
        if message.from_user.id in config.bot_admins:
            answer = await message.answer('Пожалуйста, напишите, каких пользователей вы хотите добавить в '
                                          'список операторов? \n'
                                          'Передайте в ответном сообщении их <code>user_id</code> '
                                          '(уникальные идентификаторы). \n'
                                          'Можно передавать идентификаторы списком. \n'
                                          'Например, <code>911298894 129673633 890032481</code>.')
            await AddOperatorsQuestions.first()
        else:
            answer = await message.answer(emoji.emojize(':warning: ') + 'Извините, но вы не админ!')
        await database.add_service_message(schema_name, message.message_id)
        await database.add_service_message(schema_name, answer.message_id)
    else:
        await message.answer(emoji.emojize(':warning: ') +
                             'Пожалуйста, начните сначала запись журнала для этого чата, '
                             'чтобы создать необходимые таблицы в базе данных!')


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=AddOperatorsQuestions.Q1)
async def get_operators_names(message: types.Message, state: FSMContext):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    message_text = re.findall(config.PATTERN_ID, message.text)
    dict_statuses = dict()
    for operator_id in message_text:
        try:
            member_chat_info = await message.chat.get_member(operator_id)
        except:
            dict_statuses.update({operator_id: 'пользователя нет в этом чате или не существует'})
        else:
            if await database.exists_operator_in_dict(schema_name, operator_id):
                dict_statuses.update({member_chat_info['user']['username']: 'уже есть в списке операторов чата'})
            else:
                sql = f"""INSERT INTO {schema_name}.{config.TABLE_DICT_OPERATORS} VALUES ({operator_id});"""
                await database.execute(sql, execute=True)
                dict_statuses.update({member_chat_info['user']['username']: 'добавлен в список операторов чата'})
    message_report = ''
    for status in dict_statuses:
        message_report = message_report + f'<code>{status}</code> — {dict_statuses[status]} \n'
    if message_report:
        answer = await message.answer(message_report)
    else:
        answer = await message.answer(emoji.emojize(':warning: ') +
                                      'В вашем сообщении не нашлось ничего похожего на id, попробуйте ещё раз...')
    await database.add_service_message(schema_name, message.message_id)
    await database.add_service_message(schema_name, answer.message_id)
    await state.finish()
