from aiogram import types


async def set_default_commands(dispatcher):
    await dispatcher.bot.set_my_commands([
        types.BotCommand('init', 'инициализация'),
        types.BotCommand('description', 'описание проблем'),
        types.BotCommand('records', 'получить статистику'),
        types.BotCommand('add_admins', 'добавить админов'),
        types.BotCommand('remove_admins', 'исключить из админов'),
        types.BotCommand('add_users', 'добавить операторов'),
        types.BotCommand('remove_users', 'исключить из операторов'),
        types.BotCommand('list_admins', 'список админов'),
        types.BotCommand('list_users', 'список операторов'),
        types.BotCommand('help', 'помощь по командам'),
    ])
