
import sqlite3
from datetime import datetime

import utils
from loader import dp
from main.timers import posting_startup
from src.data.config import MESSAGES, BOT_NAME
from utils.helpers import get_current_datetime
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    import filters
    filters.setup(dp)
    utils.setup(dp)

    print(MESSAGES['bot_start_msg'].format(BOT_NAME, get_current_datetime()))

    await on_startup_notify(dp)
    await set_default_commands(dp)


async def shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    from aiogram import executor, Dispatcher

    posting_startup()
    executor.start_polling(dp, on_startup=on_startup,
                           on_shutdown=shutdown)
