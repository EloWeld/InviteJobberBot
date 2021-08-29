import datetime
import json
from sqlite3 import connect
from typing import Union

import pytz
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from glQiwiApi import QiwiWrapper, YooMoneyAPI
from yoomoney import Authorize, Client

from main import finish_poll
from nav import get_user_menu
from src import CheckDB, PollDB
from src.data.config import *

from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from glQiwiApi.types import Bill

import nav
from loader import dp, bot
import qrcode


# ======================= CALLBACKS ======================= #
@dp.message_handler(state='btc_payment')
async def btc_payment2(message: types.Message, state: FSMContext):
    if not (str.isascii(message.text)):
        await message.answer('❌ Номер кошелька не корректен! ❌')
    else:
        await state.update_data(check=message.text)
        price = (await state.get_data())["price"]
        poll_id = PollDB.polls_filter('owner_id', message.from_user.id)[0]["id"]
        CheckDB.add_check(poll_id, message.from_user.id, message.text, price)
        await finish_poll(message.from_user.id, state=None, deposit=price)
        await message.answer(
                                   text=f"Ваш перевод должен быть проверен вручную администратором бота. \n"
                                        f"Ожидайте уведомления 👇\n{BTC_BANKER_WALLET}",
                                   reply_markup=nav.get_user_menu(message.from_user.id))
        await state.finish()


@dp.callback_query_handler(state='qiwi_payment')
async def callback_answer(callback: CallbackQuery, state: FSMContext):
    if 'poll:payment:qiwi' in callback.data:
        action = callback.data.split(':')[3]
        if 'check' == action:
            bill_id = (await state.get_data())["bill_id"]
            price = (await state.get_data())["price"]
            async with QIWI_WALLET as w:
                if (await w.check_p2p_bill_status(bill_id=bill_id)) == 'PAID':
                    await callback.message.answer('❤🧡💛💚💙💜🤎🖤🤍\n'
                                                  'Подписка оплачена! Теперь она будет отправлена на модерацию ♥\n'
                                                  'Не волнуйтесь, модерация занимает всего пару часов, даже в случае отклнения '
                                                  'заявки средства вернуться на карту!\n❤🧡💛💚💙💜🤎🖤🤍',
                                                  reply_markup=get_user_menu(callback.message))
                    await finish_poll(callback.from_user.id, state=state, deposit=price)
                    await callback.message.delete()
                    await state.finish()
                else:
                    try:
                        await callback.message.edit_text('Статус платежа: <b>Счёт ожидает оплаты</b>',
                                                         reply_markup=callback.message.reply_markup)
                    except:
                        await callback.message.answer('Статус платежа: <b>Счёт ожидает оплаты</b>',
                                                      reply_markup=callback.message.reply_markup)

        # =================== CANCEL ======================= #
        if 'cancel' == action:
            await callback.message.edit_text('Платёж отменен пользователем')
            await state.finish()


@dp.callback_query_handler(state='yoomoney_payment')
async def callback_answer(callback: CallbackQuery, state: FSMContext):
    price = (await state.get_data())["price"]
    client = Client(YOOMONEY_ACCESS_TOKEN)
    history = client.operation_history(label=str(callback.from_user.id))
    if 'poll:payment:yoomoney:' in callback.data:
        action = callback.data.split(':')[3]
        if action == 'check':
            print(history.operations)
            if len(history.operations) == 0:
                await callback.message.edit_text(f'Статус платежа: <b>Не оплачен</b>',
                                                 reply_markup=callback.message.reply_markup)
            elif history.operations[0].status == 'success':
                await callback.message.edit_text(f'Статус платежа: <b>Оплачен</b>',
                                                 reply_markup=None)
                await callback.message.answer('❤🧡💛💚💙💜🤎🖤🤍\n'
                                              'Подписка оплачена! Теперь она будет отправлена на модерацию ♥\n'
                                              'Не волнуйтесь, модерация занимает всего пару часов, даже в случае отклнения '
                                              'заявки средства вернуться на карту!\n❤🧡💛💚💙💜🤎🖤🤍',
                                              reply_markup=get_user_menu(callback.message))
                await finish_poll(callback.from_user.id, state=state, deposit=price)
                await callback.message.delete()
                await state.finish()
            else:
                await callback.message.edit_text(f'Статус платежа: <b>{history.operations[0].status.capitalize()}</b>',
                                                 reply_markup=callback.message.reply_markup)

        # =================== CANCEL ======================= #
        if action == 'cancel':
            await callback.message.edit_text('Платёж отменен пользователем')
            await state.finish()
