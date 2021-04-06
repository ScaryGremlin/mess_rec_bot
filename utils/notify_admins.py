from aiogram import Dispatcher

import data.config


# Уведомить администраторов о запуске бота
async def on_startup_notify(dispatcher: Dispatcher):
    for admin in data.config.admins:
        await dispatcher.bot.send_message(admin, 'Started!')
