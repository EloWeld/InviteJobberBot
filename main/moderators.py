from random import randrange

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import *
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import json
from glQiwiApi.types import Bill
from yoomoney import Quickpay

import nav
from filters import *
from loader import dp, bot
from main import finish_poll
from main.poll_controller import *
from src import PollDB, CheckDB
from src.data.config import BUTTONS, YOOMONEY, QIWI_WALLET
from states.states import *


# ======================= CALLBACKS ======================= #
@dp.callback_query_handler(state=EmployeesPoll.Payment)
async def callback_answer_poll(callback: CallbackQuery, state: FSMContext):
    # ============= POLL PAYMENT ============= #
    if 'poll:payment' in callback.data:
        if 'poll:payment:qiwi' == callback.data:
            price = (await state.get_data())["price"]
            num = hash(randrange(1, 100000))
            async with QIWI_WALLET as w:
                # Делаем p2p запрос(счёт)
                w._p2p_router.config.P2P_QIWI_HEADERS["Referrer-Policy"] = "no-referrer"
                bill = await w.create_p2p_bill(
                    amount=price,
                    comment=f'Оплата подписки в боте Скружда для Автопостинга объявлений, номер: {num}'
                )
                await state.update_data(bill_id=bill.bill_id)
                await state.update_data(bill_num=num)
            # Редачим сообщение оплаты
            await callback.message.edit_reply_markup(nav.qiwi_payment_panel(bill.pay_url))
            # Устанавливаем стейт для перехода в оплату
            await state.set_state('qiwi_payment')
        if 'poll:payment:yoomoney' == callback.data:
            price = (await state.get_data())["price"]
            quickpay = Quickpay(
                receiver=YOOMONEY,
                quickpay_form="shop",
                targets="Оплата подписки на бота",
                paymentType="SB",
                sum=price,
            )
            # Редачим сообщение оплаты
            await callback.message.edit_reply_markup(nav.yoomoney_payment_panel(quickpay.redirected_url))
            # Устанавливаем стейт для перехода в оплату
            await state.set_state('yoomoney_payment')
        if 'poll:payment:back' == callback.data:
            await callback.message.edit_reply_markup(nav.poll_payment_menu)

        if 'poll:payment:btc' == callback.data:
            price = (await state.get_data())["price"]
            await callback.message.answer(text=
f'''
Отправьте боту чек на {price} RUB
Все проверки обрабатываются в ручном режиме
''')
            await state.set_state('btc_payment')

@dp.callback_query_handler()
async def callback_answer(callback: CallbackQuery, state: FSMContext):
    sdata = callback.data.split(':')
    if 'admin:banker' in callback.data:
        action = sdata[2]
        check = sdata[3]
        poll_id = sdata[4]
        user_id = sdata[5]
        deposit = sdata[6]
        print(action, callback.data, check, poll_id)
        if 'approve' == action:
            # Изменяем статус анкеты
            try:
                await finish_poll(owner_id=user_id, deposit=deposit, state=None)
                await bot.send_message(chat_id=user_id, text=f'Ваша оплата чека {check} была подтверждена!\n'
                                                             'Сейчас анкета уйдёт на модерацию, \n'
                                                             'вы всегда можете посмотреть статус заявки в Профиле /profile')
            except:
                await callback.message.answer(f'У юзера {user_id} произошла ошибка‼')
        if 'cancel' == action:
            try:
                PollDB.polls_filter_remove('poll_id', poll_id)
                await bot.send_message(chat_id=user_id, text=f'Ваша оплата чека {check} была отклонена!\n'
                                                             'Заполните анкету заново, т.к. она аннулированна!\n'
                                                             '/find_employs')
            except:
                pass
        await callback.message.delete()
        CheckDB.remove_check(check)
    # ============= MODERATOR POLL APPROVAL ============= #
    if 'poll:approval' in callback.data:
        poll_id = sdata[3]
        action = sdata[2]
        # Process Accept Button
        if action == 'accept':
            await publish_poll(poll_id)
            await callback.message.delete()

        # Process Reject Button
        if action == 'reject':
            await RejectState.Reason.set()
            await dp.get_current().current_state().update_data(poll_id=poll_id)
            await dp.get_current().current_state().update_data(mod_username='@' + callback.from_user.username)
            await bot.send_message(callback.from_user.id,
                                   text=f'Пожалуйста, укажите причину отказа для анкеты {poll_id}')
            await callback.message.delete()


# ======================= MESSAGE HANDLERS ======================= #
@dp.message_handler(IsModerator(), state=RejectState.Reason)
async def state_poll_reject(message: Message, state: FSMContext):
    poll_id = (await state.get_data())["poll_id"]
    mod_username = (await state.get_data())["mod_username"]
    await reject_poll(poll_id, mod_username, message.text)
    await state.finish()


@dp.message_handler(Text(BUTTONS["see_polls"]), IsModerator())
@dp.message_handler(Command('polls'), IsModerator())
async def cmd_see_polls(message: Message):
    polls = PollDB.polls_filter('status', str(PollStatus.ON_MODERATION))
    # Если заявок нет
    if polls == []:
        await message.answer('🃏 Заявок нет! 🃏')
        return
    # Выводим весь список заявок и подцепляем к ним инлайны
    await message.answer('Вот список всех подписок на модерацию')
    for poll_ent in polls:
        moder_panel = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
            [
                InlineKeyboardButton(text='Отклонить', callback_data=f'poll:approval:reject:{poll_ent["id"]}'),
                InlineKeyboardButton(text='Одобрить', callback_data=f'poll:approval:accept:{poll_ent["id"]}'),
            ]
        ]
                                           )
        await message.answer(f'🎩 User {poll_ent["owner_id"]}\n'
                             f'https://t.me/{UsersDB.filter("id", poll_ent["owner_id"])[0]["username"]}\n'
                             f'======================================='
                             f'{poll_ent["vacancy"]}'
                             f'=======================================', reply_markup=moder_panel)
