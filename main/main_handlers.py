from datetime import datetime, timedelta

from aiogram.dispatcher.filters.builtin import *
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

import nav
from filters import *
from loader import dp, bot
from nav import get_user_menu
from src.data.config import BUTTONS, DECODE_POLL, PROFILE_GIF_FILEID, DATETIME_FORMAT, MESSAGES
from src.data.database import UsersDB, PollDB

# region START
from utils.helpers import get_formatted_datetime, get_subscription_diff


@dp.message_handler(IsPrivate(), Command('menu'))
async def menu(message: Message):
    await message.answer('Вот, держи меню 🌈', reply_markup=get_user_menu(message))


@dp.errors_handler()
@dp.message_handler(IsPrivate(), Text(BUTTONS["start"]))
@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: Message):
    bot_me = await bot.get_me()
    try:
        if UsersDB.get_0user_data(message.from_user.id, 'id') is None:
            UsersDB.add_user(message.from_user)
    except Exception as e:
        print(e)
    user_fullname = UsersDB.filter('id', message.from_user.id)[0]["fullname"]
    await message.answer(MESSAGES["bot_moto"].format(user_fullname),
        reply_markup=get_user_menu(message.from_user.id))


# endregion

# region MENU
@dp.message_handler(Text(BUTTONS["find_employs"]))
@dp.message_handler(Command('find_employs'))
async def cmd_find_employees(message: Message):
    # Проверяем, есть ли уже зарегестрированная анкета
    try:
        user_poll = PollDB.polls_filter('owner_id', message.from_user.id)[0]
        status = DECODE_POLL['status'][user_poll['status']]
        await message.answer(f'У вас уже есть анкета со статусом '
                             f'<b><u>{status}</u></b>!\n'
                             f'Посмотреть её можно в профиле',
                             reply_markup=get_user_menu(message))
    except:

        await message.answer(MESSAGES["poll_moto"], reply_markup=nav.start_poll_menu)


@dp.message_handler(Text(BUTTONS["chat"]))
@dp.message_handler(Command('chat'))
async def cmd_chat(message: Message):
    await message.answer('В чат с постингом вы можете перейти по ссылке ниже', reply_markup=nav.chat_link)


@dp.message_handler(Text(BUTTONS["profile"]))
@dp.message_handler(Command('profile'))
async def cmd_profile(message: Message):
    text = ''

    try:
        # Получаем анкету пользователя
        user_poll = PollDB.polls_filter('owner_id', message.from_user.id)[0]
        user = UsersDB.filter('id', message.from_user.id)[0]
        # Получаем дни до окончания и тип
        poll_status = DECODE_POLL['status'][user_poll['status']]
        pub_time = user_poll['pub_time']
        poll_sub_type = DECODE_POLL['sub_type'][user_poll['sub_type']]
        poll_diff = None
        if pub_time:
            end_day = datetime.strptime(pub_time, DATETIME_FORMAT) + timedelta(days=int(user_poll['sub_len']))
            start_day = datetime.now()
            poll_diff = get_subscription_diff(get_formatted_datetime(start_day), get_formatted_datetime(end_day))[
                0] if pub_time else None
        text = f'🎩 Профиль <b>{user["fullname"]}</b> \n' \
               f'📝 Ваш статус: <b>{user["privilege"].capitalize()}</b> \n' \
               f'☑️ Статус подписки - <b>{poll_status}</b>\n' \
               f'🖊 Тип подписки - <b>{poll_sub_type}</b>\n' + \
               (f"⏱ Осталось дней до конца подписки - <b>{poll_diff}</b>" if poll_diff is not None else '\n')
        c_menu = ReplyKeyboardMarkup(resize_keyboard=True,
                                     keyboard=nav.profile_menu.keyboard) \
            .add(KeyboardButton(text=BUTTONS['profile_my_poll']))
    except:
        # Нет анкет
        text = MESSAGES["bot_no_vacancy"]
        c_menu = nav.profile_menu

    await message.answer_document(document=PROFILE_GIF_FILEID, caption=text,
                                  reply_markup=c_menu)


# endregion

# region PROFILE

@dp.message_handler(Text(BUTTONS['profile_back']))
async def cmd_profile_back(message: Message):
    await message.answer(
        '''
            Вы в главном меню
        ''', reply_markup=get_user_menu(message))


@dp.message_handler(Text(BUTTONS['profile_my_poll']))
async def cmd_profile_my_vacancy(message: Message):
    try:
        user_poll = PollDB.polls_filter('owner_id', message.from_user.id)[0]
        await message.answer(text='Вот твоя анкета')
        await message.answer(text=user_poll["vacancy"])
        await message.answer(text='Время в которое публикуется: ' + user_poll["posting_time"])
    except Exception as e:
        await message.answer('Анкета не найдена, ошибка: ' + str(e), reply_markup=nav.profile_menu)
# endregion
