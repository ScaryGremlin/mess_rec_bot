from aiogram import Dispatcher

import data.config


# Уведомить владельца о запуске бота
async def on_startup_notify(dispatcher: Dispatcher):
    for owner in data.config.owners:
        await dispatcher.bot.send_message(owner, 'Started!')
