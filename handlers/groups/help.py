from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from data import config
from loader import database
from loader import dispatcher


@dispatcher.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    answer = await message.answer('/init — начать ведение журнала сообщений (доступна админам или владельцам); \n'
                                  '/description — инструкция о том, как оформлять сообщения, описание проблем '
                                  '(доступна в личной переписке с ботом); \n'
                                  '/records — запросить статистику по сообщениям (доступна админам или владельцам); \n'
                                  '/add_admins — добавить пользователей с <code>user_id</code> в список '
                                  'админов (доступна только владельцам); \n'
                                  '/remove_admins — исключить пользователей с <code>user_id</code> из списка админов '
                                  '(доступна только владельцам); \n'
                                  '/add_users — добавить пользователей с <code>user_id</code> в список операторов. '
                                  'Сообщения операторов в чате не удаляются (доступна админам или владельцам); \n'
                                  '/remove_users — исключить пользователей с <code>user_id</code> из списка операторов '
                                  '(доступна админам или владельцам); \n'
                                  '/list_admins — посмотреть список админов в чате '
                                  '(доступна админам или владельцам); \n'
                                  '/list_users — посмотреть список операторов в чате '
                                  '(доступна админам или владельцам); \n'
                                  '/help — прочитать это сообщение ещё раз. \n'
                                  '\n'
                                  'Если что-то идет не так и вы не понимаете, как такое возможно, '
                                  'пожалуйста, напишите @arthur_dzhemakulov.')
    await database.add_service_message(schema_name, message.message_id)
    await database.add_service_message(schema_name, answer.message_id)
