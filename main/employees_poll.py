from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

import nav
from filters import IsPrivate, UsersDB
from loader import dp, bot
from main import validators
from nav import get_user_menu
from src import PollDB
from src.data.config import DECODE_POLL, MESSAGES, REPLACES, PRICELIST, PRICE_COLOR_MULTIPLY, BUTTONS, PollStatus
from states import EmployeesPoll, State


async def change_poll_status(poll_id, status: PollStatus, state: FSMContext = None):
    if state:
        await state.update_data(status=str(status))
    PollDB.update_status(poll_id, str(status))


# ======================= HANDLERS ======================= #
@dp.message_handler(IsPrivate(), Text('☕️Приступить'))
async def cmd_poll_start(message: Message):
    # Проверяем, есть ли уже зарегестрированная анкета
    try:
        user_poll = PollDB.polls_filter('owner_id', message.from_user.id)[0]
        status = DECODE_POLL['status'][user_poll['status']]
        await message.answer(f'У вас уже есть анкета со статусом '
                             f'<b><u>{status}</u></b>!\n'
                             f'Посмотреть её можно в профиле',
                             reply_markup=get_user_menu(message))
    except:
        msg = await message.answer(MESSAGES['poll_color_lbl'], reply_markup=nav.poll_color_menu)

        await EmployeesPoll.Color.set()
        state = dp.get_current().current_state()
        await state.update_data(poll_msgs=[[EmployeesPoll.Color, msg]])


async def save_msg(msg: Message, state: State(), replymsg: Message = None):
    data = (await dp.get_current().current_state().get_data())["poll_msgs"]
    await dp.get_current().current_state().update_data(poll_msgs=data + [[state, msg]])
    if replymsg:
        await dp.get_current().current_state().update_data(poll_msgs=data + [[state, msg], [state, replymsg]])


async def btn_cancel(message: Message, state: FSMContext):
    await message.delete()
    data = (await state.get_data())["poll_msgs"]
    for msg in data:
        try:
            await msg[1].delete()
        except:
            pass
    await message.answer('❌ Вы отменили заполнение заявки ❌',
                         reply_markup=get_user_menu(message.from_user.id))
    await state.finish()
    return


async def btn_back(message: Message, state: State(), l_state: State()):
    await message.delete()
    data = (await dp.get_current().current_state().get_data())["poll_msgs"]
    new_data = []
    msg = None
    [print(x[0], state, l_state) for x in data]
    for tp in data:
        if tp[0].state in [state.state, l_state.state]:
            await tp[1].delete()
        else:
            new_data += [tp]
    for tp in range(len(data)):
        if data[tp][0].state == l_state.state:
            msg = await bot.send_message(chat_id=message.from_user.id,
                                         text=data[tp][1].text,
                                         reply_markup=data[tp][1].reply_markup)
            break
    await dp.get_current().current_state().update_data(poll_msgs=(new_data + [[l_state, msg]]) if msg else new_data)
    await l_state.set()
    return


# ========== COLOR =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.Color)
async def cmd_poll_color(message: Message, state: FSMContext):
    if message.text in [BUTTONS['btn_back'], BUTTONS['btn_cancel']]:
        await btn_cancel(message, state)
        return
    if await validators.validate_poll_color(message.text):
        # Initialize Poll
        msg = await message.answer(MESSAGES['poll_difficulty_lbl'], reply_markup=nav.poll_diff_menu)
        await save_msg(msg, EmployeesPoll.Color, message)

        await state.update_data(color=REPLACES[message.text])
        await state.update_data(status=str(PollStatus.EDITING))
        await state.update_data(owner_id=message.from_user.id)
        await EmployeesPoll.Difficulty.set()
    else:
        msg = await message.answer(MESSAGES['invalid_input'], reply_markup=nav.poll_color_menu)
        await save_msg(msg, EmployeesPoll.Color, message)
        await EmployeesPoll.Color.set()


# ========== DIFFICULTY =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.Difficulty)
async def cmd_poll_diff(message: Message, state: FSMContext):
    if message.text == BUTTONS['btn_cancel']:
        await btn_cancel(message, state)
        return
    if message.text == BUTTONS['btn_back']:
        await btn_back(message, EmployeesPoll.Difficulty, EmployeesPoll.Color)
        return

    if await validators.validate_poll_difficulty(message.text):
        msg = await message.answer(MESSAGES['poll_wages_lbl'], reply_markup=nav.back_cancel_menu)
        await save_msg(msg, EmployeesPoll.Difficulty, message)

        await state.update_data(difficulty=REPLACES[message.text])
        await EmployeesPoll.Wages.set()
    else:
        msg = await message.answer(MESSAGES['invalid_input'], reply_markup=nav.poll_diff_menu)
        await save_msg(msg, EmployeesPoll.Difficulty, message)

        await EmployeesPoll.Difficulty.set()


# ========== WAGES =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.Wages)
async def cmd_poll_wages(message: Message, state: FSMContext):
    if message.text == BUTTONS['btn_cancel']:
        await btn_cancel(message, state)
        return
    if message.text == BUTTONS['btn_back']:
        await btn_back(message, EmployeesPoll.Wages, EmployeesPoll.Difficulty)
        return

    msg = await message.answer(MESSAGES['poll_time_lbl'], reply_markup=nav.back_cancel_menu)
    await save_msg(msg, EmployeesPoll.Wages, message)

    await state.update_data(wages=message.text)

    await EmployeesPoll.Time.set()


# ========== TIME =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.Time)
async def cmd_poll_time(message: Message, state: FSMContext):
    if message.text == BUTTONS['btn_cancel']:
        await btn_cancel(message, state)
        return
    if message.text == BUTTONS['btn_back']:
        await btn_back(message, EmployeesPoll.Time, EmployeesPoll.Wages)
        return

    msg = await message.answer(MESSAGES['poll_desc_lbl'], reply_markup=nav.back_cancel_menu)
    await save_msg(msg, EmployeesPoll.Time, message)

    await state.update_data(time=message.text)

    await EmployeesPoll.Description.set()


# ========== DESCRIPTION =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.Description)
async def cmd_poll_description(message: Message, state: FSMContext):
    if message.text == BUTTONS['btn_cancel']:
        await btn_cancel(message, state)
        return
    if message.text == BUTTONS['btn_back']:
        await btn_back(message, EmployeesPoll.Description, EmployeesPoll.Time)
        return

    if not await validators.validate_poll_description(message.text):
        msg = await message.answer('Некорректный ввод, попробуйте ещё раз!')
        await save_msg(msg, EmployeesPoll.Description, message)

        await EmployeesPoll.Description.set()
        return

    msg = await message.answer('6️⃣ Связь в формате @username:',
                               reply_markup=nav.poll_contact_menu(message.from_user.username))
    await save_msg(msg, EmployeesPoll.Description, message)
    await state.update_data(desc=message.text)

    await EmployeesPoll.Contact.set()


# ========== CONTACT =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.Contact)
async def cmd_poll_contact(message: Message, state: FSMContext):
    if message.text == BUTTONS['btn_cancel']:
        await btn_cancel(message, state)
        return
    if message.text == BUTTONS['btn_back']:
        await btn_back(message, EmployeesPoll.Contact, EmployeesPoll.Description)
        return

    if not await validators.validate_poll_contact(message.text):
        msg = await message.answer('Некорректный ввод, попробуйте ещё раз!')
        await save_msg(msg, EmployeesPoll.Contact, message)

        await EmployeesPoll.Contact.set()
        return

    await state.update_data(contact=message.text)

    data = await state.get_data()

    await state.update_data(vacancy=MESSAGES["vacancy_preview"]
                            .format(data["color"], data["difficulty"], data["wages"],
                                    data["time"], data["desc"], data["contact"]))

    data = await state.get_data()
    msg = await message.answer('Отлично! Анкета заполнена, превью ниже:\n' + data["vacancy"],
                               reply_markup=nav.poll_confirm_menu)
    await save_msg(msg, EmployeesPoll.Contact, message)

    await message.answer('Всё верно?👇')

    await EmployeesPoll.Confirm.set()


# ========== CONFIRM =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.Confirm)
async def cmd_poll_confirm(message: Message, state: FSMContext):
    if message.text == BUTTONS['btn_back']:
        await btn_back(message, EmployeesPoll.Confirm, EmployeesPoll.Contact)
        return
    elif message.text == BUTTONS["pconfirm_next"]:
        [await msg[1].delete() for msg in (await state.get_data())["poll_msgs"]]
        await message.answer(MESSAGES["sub_type_moto"],
                             reply_markup=nav.poll_subs_type)
        await EmployeesPoll.SubscriptionType.set()
    elif message.text == BUTTONS["pconfirm_again"]:
        await message.answer('Хорошо, заполняй заново',
                             reply_markup=nav.poll_color_menu)
        await EmployeesPoll.Color.set()
    else:
        await message.answer('Некорректный ввод, попробуйте ещё раз!',
                             reply_markup=nav.poll_confirm_menu)
        await EmployeesPoll.Confirm.set()


# ========== SUBSCRIPTION TYPE =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.SubscriptionType)
async def cmd_poll_confirm(message: Message, state: FSMContext):
    sub_type = 1
    if message.text == '🔎 Обычная':
        sub_type = 1
    elif message.text == '🎖 Premium':
        sub_type = 2
    else:
        await message.answer('Некорректный ввод, попробуйте ещё раз!',
                             reply_markup=nav.poll_subs_type)
        await EmployeesPoll.SubscriptionType.set()
        return

    await state.update_data(sub_type=sub_type)
    poll_data = await state.get_data()
    mult = PRICE_COLOR_MULTIPLY[poll_data["color"]]

    await message.answer('<b>Выберите период действия подписки:</b>\n'
                         f'• На 3 дня — <u>{PRICELIST[sub_type][3] * mult}</u>₽\n'
                         f'• На неделю — <u>{PRICELIST[sub_type][7] * mult}</u>₽\n'
                         f'• На месяц — <u>{PRICELIST[sub_type][30] * mult}</u>₽\n', reply_markup=nav.poll_subs_length)
    await EmployeesPoll.SubscriptionLength.set()


# ========== SUBSCRIPTION LENGTH =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.SubscriptionLength)
async def cmd_poll_confirm(message: Message, state: FSMContext):
    try:
        await state.update_data(sub_len=REPLACES[message.text])
    except:
        await message.answer('Некорректный ввод, попробуйте ещё раз!',
                             reply_markup=nav.poll_subs_length)
        await EmployeesPoll.SubscriptionLength.set()
        return

    await message.answer('Введите время в которое будет публиковаться заявка\n'
                         '• Обычный формат - \" ХХ:ХХ\"\n'
                         '• Премиум формат - \" ХХ:ХХ XX:XX\"\n')
    await EmployeesPoll.PostingTime.set()


# ========== POSTING TIME =========== #
@dp.message_handler(IsPrivate(), state=EmployeesPoll.PostingTime)
async def cmd_posting_time(message: Message, state: FSMContext):
    poll_data = await state.get_data()
    posting_time = "00-00"
    times = validators.validate_poll_post_time(message.text, poll_data['sub_type'])
    if times:
        posting_time = times
        await state.update_data(posting_time=posting_time)
        await message.answer(f'Установленые часы: {posting_time}')
    else:
        await message.answer('Некорректный ввод, попробуйте ещё раз!',
                             reply_markup=None)
        await EmployeesPoll.PostingTime.set()
        return

    poll_data = await state.get_data()
    poll_price = PRICELIST[poll_data['sub_type']][poll_data['sub_len']] * PRICE_COLOR_MULTIPLY[poll_data['color']]
    await state.update_data(price=poll_price)

    # Записываем изменения в БДstatus=status=
    await state.update_data(status=str(PollStatus.PAYMENT))
    data = await state.get_data()
    PollDB.save_poll(data)

    # Отсылаем запрос на оплату
    await message.answer('✅ Отлично, анкета полностью заполнена! Осталось только её оплатить 💳')
    await EmployeesPoll.Payment.set()
    await message.answer('Выберите платежную систему:', reply_markup=nav.poll_payment_menu)


async def finish_poll(owner_id, state=None, deposit: int = 0):
    # Обновляем записи в бд
    user_deposit = int(UsersDB.get_0user_data(owner_id, 'deposit'))
    UsersDB.update_field(owner_id, 'deposit', user_deposit + int(deposit))

    poll_data = PollDB.polls_filter('owner_id', owner_id)[0]
    await bot.send_message(chat_id=owner_id, text=
    'Поздравляем, подписка оформлена и ваша анкета отправлена на модерацию!\n'
    'Вы можете проверить её в профиле /profile')
    await change_poll_status(poll_data["id"], PollStatus.ON_MODERATION)
    if state:
        await state.finish()
