from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.data.config import *

poll_subscription_type = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text=BUTTONS["sub_type_1"], callback_data='sub_type_1'),
        InlineKeyboardButton(text=BUTTONS["sub_type_2"], callback_data='sub_type_2'),
    ]
]
                                              )

chat_link = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text=BUTTONS["chat_link"], url=CHAT_LINK),
    ]
]
                                 )

poll_payment_menu = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text='QIWI | Карта', callback_data='poll:payment:qiwi'),
        InlineKeyboardButton(text='Юмани | Карта', callback_data='poll:payment:yoomoney'),
    ],
    [
        InlineKeyboardButton(text='BTC Banker', callback_data='poll:payment:btc'),
    ]
]
                                         )
def btc_payment_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='💳 Оплатить', callback_data='poll:payment:btc'),
        ],
        [
            InlineKeyboardButton(text='⬅ Назад', callback_data='poll:payment:back')
        ]
    ])

def get_banker(check):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Одобрить подписку', callback_data=f'admin:banker:approve:{check["check"]}:{check["poll_id"]}:{check["owner_id"]}:{check["price"]}'),
        ],
        [
            InlineKeyboardButton(text='Отменить', callback_data=f'admin:banker:cancel:{check["check"]}:{check["poll_id"]}:{check["owner_id"]}:{check["price"]}')
        ]
    ])

def qiwi_payment_panel(data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='🥝 Оплатить', url=data),
            InlineKeyboardButton(text='🔎 Проверить оплату', callback_data='poll:payment:qiwi:check')
        ],
        [
            InlineKeyboardButton(text='🚫 Отменить', callback_data='poll:payment:qiwi:cancel')
        ],
        [
            InlineKeyboardButton(text='⬅ Назад', callback_data='poll:payment:back')
        ]
    ])


def yoomoney_payment_panel(data):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='💳 Оплатить', url=data),
            InlineKeyboardButton(text='🔎 Проверить оплату', callback_data='poll:payment:yoomoney:check')
        ],
        [
            InlineKeyboardButton(text='🚫 Отменить', callback_data='poll:payment:yoomoney:cancel')
        ],
        [
            InlineKeyboardButton(text='⬅ Назад', callback_data='poll:payment:back')
        ]
    ])
