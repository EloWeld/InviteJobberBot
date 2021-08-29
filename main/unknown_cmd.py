
from main import *
from src.data.config import *


@dp.message_handler(IsPrivate())
async def cmd_poll_start(message: Message):
    await message.answer(MESSAGES['unknow_cmd'], reply_markup=nav.get_user_menu(message.from_user.id))
