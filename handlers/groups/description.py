from aiogram import types
from aiogram.dispatcher.filters import Command

from data import config
from loader import database
from loader import dispatcher


@dispatcher.message_handler(Command('description'))
async def bot_description(message: types.Message):
    schema_name = config.SCHEMA + str(message.chat.id).replace('-', '')
    answer = await message.answer('<b>Как оформлять сообщения?</b> \n'
                                  'Сообщение должно начинаться с символа <code>#</code> и далее — номер хаба, '
                                  'город и номер проблемы, разделённые символом "косая черта" — <code>/</code>. \n'
                                  'Например, <code>#340/Москва/4</code>, где: \n'
                                  '<code>#</code> — символ, говорящий о том, что вы обращаетесь с проблемой; \n'
                                  '<code>340</code> — номер хаба; \n'
                                  '<code>Москва</code> — город размещения хаба; \n'
                                  '<code>4</code> — номер проблемы по классификатору. \n'
                                  '\n'
                                  '<b>Нумерация проблем для обращения в чат КЦ:</b> \n'
                                  '<code>1</code> — если клиент утверждает, что оплатил заказ онлайн, '
                                  'а вы его не видите в программе; \n'
                                  '<code>2</code> — упал один заказ с онлайн оплатой, '
                                  'а второй, идентичный первому, за наличные; \n'
                                  '<code>3</code> — аптека будет закрыта; \n'
                                  '<code>4</code> — нет света и нет возможности выставить проблемный статус; \n'
                                  '<code>5</code> — курьер на выдаче или клиент у кассы, '
                                  'уточнить снятие проблемы по заказу. \n'
                                  '\n'
                                  'Пожалуйста, обращайте внимание на символы пробела! \n'
                                  'К примеру, сообщение \n'
                                  '<code># 250/Волгоград/ 4</code> оформлено не верно! \n'
                                  )
    if await database.exists_schema(schema_name):
        await database.add_service_message(schema_name, message.message_id)
        await database.add_service_message(schema_name, answer.message_id)
