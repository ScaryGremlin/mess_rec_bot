from aiogram import Dispatcher

from data import config
from loader import dispatcher
from loader import scheduler


async def send_message_to_admin(dp: Dispatcher):
    for admin in config.bot_admins:
        await dp.bot.send_message(admin, 'Сообщение по таймеру')


def schedule_jobs():
    scheduler.add_job(send_message_to_admin, 'interval', seconds=config.SEC_CLEAR, args=(dispatcher,))
