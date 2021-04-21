from aiogram import types


async def set_default_commands(dispatcher):
    await dispatcher.bot.set_my_commands([
        types.BotCommand('description', 'описание проблем'),
        types.BotCommand('init', 'начало записи журнала'),
        types.BotCommand('records', 'получить статистику'),
        types.BotCommand('add_operators', 'добавить операторов'),
        types.BotCommand('remove_operators', 'исключить из операторов'),
        types.BotCommand('list_operators', 'список операторов'),
        types.BotCommand('delete', 'удалить сообщения бота и команды'),
        types.BotCommand('help', 'помощь по командам'),
    ])
