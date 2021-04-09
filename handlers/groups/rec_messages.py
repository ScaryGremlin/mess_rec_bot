import re

from aiogram import types

from data import config
from loader import database
from loader import dispatcher

pattern_problem = re.compile(r'[#]\d+[/][0-9а-яА-Яa-zA-ZёЁ\s+-]+[/][1-6]')


@dispatcher.message_handler(regexp=pattern_problem, state=None)
async def rec_re(message: types.Message):
    result_problem = pattern_problem.search(message.text)
    dict_problem = result_problem.group(0).split('/')
    hub = dict_problem[0].replace('#', '')
    city = dict_problem[1].replace(' ', '')
    number_problem = dict_problem[2]
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    user_name = message.from_user.username
    message_text = message.text
    date_time = message.date
    shema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    if await database.exists_schema(shema_name):
        sql = f"""INSERT INTO {shema_name}.{config.MESSAGES_STRUCT} 
            (hub, city, number_problem, user_id, full_name, user_name, message_text, date_time)
            VALUES ({hub}, '{city}', {number_problem}, {user_id}, '{full_name}', 
                '{user_name}', '{message_text}', '{date_time}')
        """
        await database.execute(sql, execute=True)
    else:
        pass


@dispatcher.message_handler(content_types='text', state=None)
async def delete_message(message: types.Message):
    print(message.chat.id, message.message_id)
    await message.delete()


# @dispatcher.message_handler(content_types='text', state=None)
# async def rec_rest(message: types.Message):
#     user_id = message.from_user.id
#     full_name = message.from_user.full_name
#     user_name = message.from_user.username
#     date_time = message.date
#     message_text = message.text
#     shema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
#     if await database.exists_schema(shema_name):
#         sql = f"""INSERT INTO {shema_name}.{config.MESSAGES_UNSTRUCT}
#             (user_id, full_name, user_name, message_text, date_time)
#             VALUES ({user_id}, '{full_name}', '{user_name}', '{message_text}', '{date_time}')
#         """
#         await database.execute(sql, execute=True)
#     else:
#         pass
