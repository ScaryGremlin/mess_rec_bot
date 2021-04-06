from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from loader import dispatcher


@dispatcher.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer('/init — инициализация, начало записи в базу (доступно только администраторам); \n'
                         '/description — инструкция о том, как оформлять сообщения, описание проблем; \n'
                         '/records — запросить статистику по сообщениям (доступно только администраторам); \n'
                         '/help — прочитать это сообщение ещё раз. \n'
                         '\n'
                         'Если что-то идет не так и вы не понимаете, как такое возможно, '
                         'пожалуйста, напишите @arthur_dzhemakulov.')
