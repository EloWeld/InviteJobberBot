from aiogram.types import Message

import nav
from filters import IsPrivate
from loader import dp
from src.data.config import MESSAGES


@dp.message_handler(IsPrivate())
async def cmd_poll_start(message: Message):
    await message.answer(MESSAGES['unknow_cmd'], reply_markup=nav.get_user_menu(message.from_user.id))
