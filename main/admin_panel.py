from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import *
from aiogram.types import Message
from yoomoney import Client

import nav
from filters import *
from loader import dp
from main import validators, change_poll_status, finish_poll
from main.poll_controller import *
from src import PollDB, UsersDB, CheckDB
from src.data.config import *
from states.states import *


# =============== STATISTICS ============= #
@dp.message_handler(IsAdmin(), Text(BUTTONS["statistics"]))
@dp.message_handler(IsAdmin(), Command('stats'))
async def cmd_admin_stats(message: Message):
    users = UsersDB.all_users()
    users_count = len(users)
    users_total_deposit = sum([x["deposit"] for x in users])
    active_polls = len(PollDB.polls_filter('status', str(PollStatus.ACTIVE)))
    mod_polls = len(PollDB.polls_filter('status', str(PollStatus.ON_MODERATION)))
    await message.answer(text=MESSAGES["bot_statistics"].
                         format(users_count, users_total_deposit, active_polls, mod_polls))


# =============== Banker Menu ============= #
@dp.message_handler(IsAdmin(), Text(BUTTONS["admin_back"]))
async def admin_payments_menu(message: Message):
    await message.answer('🀄 Админка', reply_markup=nav.get_user_menu(message.from_user.id))

@dp.message_handler(IsAdmin(), Text(BUTTONS["admin_payments_menu"]))
async def admin_payments_menu(message: Message):
    await message.answer('💹 Меню платежей', reply_markup=nav.admin_payments_menu)


@dp.message_handler(IsAdmin(), Text(BUTTONS["admin_users_menu"]))
async def admin_users_menu(message: Message):
    await message.answer('💹 Меню управления пользователями', reply_markup=nav.admin_users_menu)


@dp.message_handler(IsAdmin(), Text(BUTTONS["admin_btc_banker"]))
@dp.message_handler(IsAdmin(), Command('/banker'))
async def cmd_btc_banker(message: Message):
    checks = CheckDB.all_checks()
    if len(checks) > 0:
        await message.answer('Список платежей по банкиру:')
    else:
        await message.answer('❌ Платежей по банкиру нет ❌')


    for check in checks:
        username = UsersDB.filter('id', check["owner_id"])[0]["username"]
        await message.answer(text=f'@{username} хочет оплатить подписку банкиром. Чек в сообщении ниже ⬇\n')
        await message.answer(text=f'{check["check"]}\n', reply_markup=nav.get_banker(check))


# =============== ADD ADMIN ============= #
@dp.message_handler(IsAdmin(), Text(BUTTONS["add_admin"]))
@dp.message_handler(IsAdmin(), Command('add_admin'))
async def cmd_add_admin(message: Message):
    arg = message.get_args()
    if arg is not None:
        if await validators.validate_poll_contact(arg):
            await add_admin(message)
            return
    await message.answer(MESSAGES["new_admin_username"])

    await AdminState.Admin.set()


@dp.message_handler(IsAdmin(), state=AdminState.Admin)
async def state_add_admin(message: Message, state: FSMContext):
    if await add_admin(message):
        await state.finish()


# =============== ADD MODERATOR ============= #
@dp.message_handler(IsAdmin(), Text(BUTTONS["add_moder"]))
@dp.message_handler(IsAdmin(), Command('add_moderator'))
async def cmd_add_moderator(message: Message):
    arg = message.get_args()
    if arg is not None:
        if await validators.validate_poll_contact(arg):
            await add_moder(message)
            return
    await message.answer(MESSAGES["new_moder_username"])

    await AdminState.Moder.set()


@dp.message_handler(IsAdmin(), state=AdminState.Moder)
async def state_add_moderator(message: Message, state: FSMContext):
    if await add_moder(message):
        await state.finish()


# =============== BAN ============= #
@dp.message_handler(IsAdmin(), Text(BUTTONS["admin_panel_ban"]))
@dp.message_handler(IsAdmin(), Command('ban'))
async def cmd_admin_ban(message: Message):
    await message.answer(text=MESSAGES["ban_username"])
    await AdminState.Ban.set()


@dp.message_handler(IsAdmin(), state=AdminState.Ban)
async def state_admin_ban(message: Message, state: FSMContext):
    if await validators.validate_poll_contact(message.text):
        if len(UsersDB.filter('username', message.text[1:])) > 0:
            user_x = UsersDB.filter('username', message.text[1:])[0]
            PollDB.polls_filter_remove('owner_id', user_x["id"])
            UsersDB.filter_remove('id', user_x["id"])
        else:
            await message.answer(text=MESSAGES["unknown_db_user"], reply_markup=nav.admin_menu)

    else:
        await message.answer(text=MESSAGES["unknown_db_user"], reply_markup=nav.admin_menu)

    await state.finish()


# =============== ADMIN SEE PAYMENTS ============= #
@dp.message_handler(IsAdmin(), Text(BUTTONS["admin_check_payments"]))
@dp.message_handler(IsAdmin(), Command('admin_check_payments'))
async def admin_check_payments(message: types.Message):
    await message.answer(f'Счёт на Киви: {(await  QIWI_WALLET.get_balance()).amount} RUB')
    client = Client(YOOMONEY_ACCESS_TOKEN)

    await message.answer(f'Счёт на Юмани: {client.account_info().balance} RUB')

    if len(client.operation_history().operations) > 0:
        await message.answer(f'Операции на Юмани:')

        [await message.answer(f'Вот: {x} ') for x in client.operation_history().operations]
    await message.answer(f'❌ Операций на Юмани нет ❌')


# =============== ADD CHANGE SUB ============= #
# Увеличивает количество дней подписки у юзера
@dp.message_handler(IsAdmin(), Text(BUTTONS["admin_panel_magic"]))
@dp.message_handler(IsAdmin(), Command('change_sub'))
async def cmd_admin_magic(message: Message):
    await message.answer(text='Введите точный username в формате @username')
    await AdminState.Username.set()


@dp.message_handler(IsAdmin(), state=AdminState.Username)
async def state_admin_magic(message: Message, state: FSMContext):
    if await validators.validate_poll_contact(message.text):
        if len(UsersDB.filter('username', message.text[1:])) > 0:
            await state.update_data(username=message.text[1:])
            await message.answer(text='Введите новое количество дней подписки')
            await AdminState.Changes.set()
        else:
            await message.answer(text=MESSAGES["unknown_db_user"], reply_markup=nav.admin_menu)
            await state.finish()
    else:
        await message.answer(MESSAGES["invalid_input"], reply_markup=nav.admin_menu)
        await state.finish()


@dp.message_handler(IsAdmin(), state=AdminState.Changes)
async def state_admin_magic2(message: Message, state: FSMContext):
    try:
        user_x = UsersDB.filter('username', (await state.get_data())['username'])[0]
        PollDB.update_poll_field2(user_x["id"], 'sub_len', str(message.text))
        await message.answer(f'Теперь подписка {user_x["username"]} равна {message.text} дней!')
        await state.finish()
    except:
        await message.answer(MESSAGES["invalid_input"], reply_markup=nav.admin_menu)
        await state.finish()


# ==================== BACKEND ================== #
async def add_moder(message: types.Message):
    username = message.text[1:]
    if await validators.validate_poll_contact(f'@{username}') and \
            UsersDB.get_0user_data(username, 'privilege', 'username') in ['user', 'moderator']:
        # Обновляем запись в бд
        users = UsersDB.filter('username', username)
        UsersDB.update_field(users[0]["id"], 'privilege', 'moderator')
        # Уведомляем кого админ сделал админом
        await message.answer(text=MESSAGES["moder_notify_sender"].format(username))
        # Отсылаем ноушн к юзеру, получившему
        await bot.send_message(chat_id=users[0]["id"], text=MESSAGES["moder_notify"].format(message.from_user.username))
        return True
    else:
        await message.answer(text=MESSAGES["unknown_db_user"])
        return False


async def add_admin(message: types.Message):
    username = message.text[1:]
    if await validators.validate_poll_contact(f'@{username}') and \
            UsersDB.get_0user_data(username, 'privilege', 'username') is not None:
        # Обновляем запись в бд
        users = UsersDB.filter('username', username)
        UsersDB.update_field(users[0]["id"], 'privilege', 'admin')
        # Уведомляем кого админ сделал админом
        await message.answer(text=MESSAGES["admin_notify_sender"].format(username))
        # Отсылаем ноушн к юзеру, получившему
        await bot.send_message(chat_id=users[0]["id"], text=MESSAGES["admin_notify"].format(message.from_user.username))
        return True
    else:
        await message.answer(text=MESSAGES["unknown_db_user"])
        return False
