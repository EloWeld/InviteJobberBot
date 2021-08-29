import logging
from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup

import nav
from src.data.config import superadmin, BOT_NAME, MESSAGES


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(superadmin,
                                  MESSAGES['bot_start_msg'].format(BOT_NAME, datetime.now()) +
                                  '\nType /start',
                                  disable_notification=True,
                                  reply_markup=nav.start_menu)
    except Exception as err:
        logging.exception(err)
