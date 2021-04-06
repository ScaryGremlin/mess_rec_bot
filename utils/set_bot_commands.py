from aiogram import types


async def set_default_commands(dispatcher):
    await dispatcher.bot.set_my_commands([
        types.BotCommand('init', 'инициализация'),
        types.BotCommand('description', 'описание проблем'),
        types.BotCommand('records', 'получить статистику'),
        types.BotCommand('help', 'помощь по командам'),
    ])
