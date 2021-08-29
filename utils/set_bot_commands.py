from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("start", "Запустить бота"),
        BotCommand("menu", "Главное меню"),
        BotCommand("find_employs", "Найти работников"),
        BotCommand("profile", "Меню профиля"),
    ])


async def set_exit_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("stop", "Выйти из режима")
    ])
