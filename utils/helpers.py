import asyncio
from datetime import datetime

import requests
from aiogram import types

from src.data.config import DATETIME_FORMAT, TIME_FORMAT


async def del_message(message: types.Message, time_in_milliseconds: int):
    await asyncio.sleep(time_in_milliseconds)
    await message.delete()


def get_current_datetime(date_format=DATETIME_FORMAT):
    return datetime.now().strftime(date_format)


def get_formatted_datetime(format_date, date_format=DATETIME_FORMAT):
    return format_date.strftime(date_format)


def get_current_time(date_format=TIME_FORMAT):
    return datetime.now().strftime(date_format)


def price_to_btc(price: int):
    return requests.get(url='https://blockchain.info/tobtc', params={
        'currency': 'RUB',
        'value': price
    }).text

class BroadcastTimer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()


# Вычисляем разницу между текущим временем и временем оформления подписки
def get_subscription_diff(a_date, b_date=get_current_datetime()):
    now = datetime.strptime(b_date, DATETIME_FORMAT)
    post_time = datetime.strptime(a_date, DATETIME_FORMAT)
    diff = (now - post_time)
    return diff.days, diff.seconds / 60 / 60  # days and hours