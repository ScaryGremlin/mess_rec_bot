from aiogram import executor

from schedulers.scheduler_del_bot_messages import schedule_jobs
from loader import database
from loader import dispatcher
from loader import scheduler
from utils.notify_bot_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import handlers


async def on_startup(dispatcher):
    # Подключиться к базе данных
    await database.connect()

    # Уведомить админов о запуске бота
    await on_startup_notify(dispatcher)

    # Установить команды
    await set_default_commands(dispatcher)

    # Запустить задачи планировщика
    schedule_jobs()

if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dispatcher, on_startup=on_startup)
