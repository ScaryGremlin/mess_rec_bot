import re

import emoji
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters import ContentTypeFilter
from aiogram.dispatcher.storage import FSMContext

from data import config
from loader import database
from loader import dispatcher
from states import DelOperatorsQuestions


@dispatcher.message_handler(Command('del_operators'))
async def del_operators(message: types.Message):

    # Имя схемы базы данных - schema_{chat_id}
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')

    # Если схема базы данных существует (если выполнена команда init)
    if await database.exists_schema(schema_name):

        # Если сообщение от админов
        if message.from_user.id in config.bot_admins:
            answer = await message.answer('Пожалуйста, напишите, каких пользователей вы хотите исключить из '
                                          'списка операторов? \n'
                                          'Передайте в ответном сообщении их <code>user_id</code> '
                                          '(уникальные идентификаторы). \n'
                                          'Можно передавать идентификаторы списком. \n'
                                          'Например, <code>911298894 129673633 890032481</code>.')
            await DelOperatorsQuestions.first()
        else:
            answer = await message.answer(emoji.emojize(':warning: ') + 'Извините, но вы не админ!')

        # Записать сообщение от бота и команду пользователя в сервисную таблицу базы данных
        await database.add_service_message(schema_name, message.message_id)
        await database.add_service_message(schema_name, answer.message_id)

    else:
        await message.answer(emoji.emojize(':warning: ') +
                             'Пожалуйста, начните сначала запись журнала для этого чата, '
                             'чтобы создать необходимые таблицы в базе данных!')


@dispatcher.message_handler(ContentTypeFilter(types.ContentType.TEXT), state=DelOperatorsQuestions.Q1)
async def get_operators_names(message: types.Message, state: FSMContext):

    # Имя схемы базы данных - schema_{chat_id}
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')

    # Найти в сообщении всё, что похоже на id пользователя по шаблону регулярного выражения
    message_text = re.findall(config.PATTERN_ID, message.text)

    # Словарь для формирования отчётного сообщения
    dict_statuses = dict()

    # Пройтись по id операторов, выбранных из сообщения
    for operator_id in message_text:

        # Если id оператора есть в таблице, то удалить его, выполнив запрос в базу
        if await database.exists_operator_in_dict(schema_name, operator_id):
            sql = f"""
                DELETE FROM {schema_name}.{config.TABLE_DICT_OPERATORS} WHERE operator_id = {operator_id};
            """
            await database.execute(sql, execute=True)

            # Если пользователь с id состоит в чате, то записать в словарь
            # отчётного сообщения его username, иначе записать id
            try:
                member_chat_info = await message.chat.get_member(operator_id)
            except:
                dict_statuses.update({operator_id: 'удалён из списка операторов чата'})
            else:
                dict_statuses.update({member_chat_info['user']['username']: 'удалён из списка операторов чата'})

        # Если id оператора нет в таблице, то записать в словарь соответствующий отчёт
        else:
            dict_statuses.update({operator_id: 'не состоит в списке операторов чата или не существует'})

    # Сформировать отчётное сообщение
    message_report = ''
    for status in dict_statuses:
        message_report = message_report + f'<code>{status}</code> — {dict_statuses[status]} \n'
    if message_report:
        answer = await message.answer(message_report)
    else:
        answer = await message.answer(emoji.emojize(':warning: ') +
                                      'В вашем сообщении не нашлось ничего похожего на id, попробуйте ещё раз...')

    # Записать сообщение от бота и команду пользователя в сервисную таблицу базы данных
    await database.add_service_message(schema_name, message.message_id)
    await database.add_service_message(schema_name, answer.message_id)

    await state.finish()
