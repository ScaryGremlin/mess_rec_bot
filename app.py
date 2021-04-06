from aiogram import executor

from loader import database
from loader import dispatcher
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import handlers


async def on_startup(dispatcher):
    # Подключиться к базе данных
    await database.connect()

    # Уведомить администратора о запуске бота
    await on_startup_notify(dispatcher)

    # Установить команды
    await set_default_commands(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_startup=on_startup)
