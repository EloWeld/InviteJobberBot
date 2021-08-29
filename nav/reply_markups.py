from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.data.config import BUTTONS

# ============================= START ==================================== #
start_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['start']),
    ]
])

# ============================= OTHER ==================================== #
next_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['next']),
    ]
])
back_cancel_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['btn_back']),
        KeyboardButton(text=BUTTONS['btn_cancel']),
    ]
])

# ============================= GENERAL MENUs ==================================== #
find_employees_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['find_employs']),
        KeyboardButton(text=BUTTONS['profile']),
        KeyboardButton(text=BUTTONS['chat']),
    ]
])
# ==== Admin menu ==== #
admin_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS["statistics"]),
    ],
    [
        KeyboardButton(text=BUTTONS["admin_panel_magic"]),
        KeyboardButton(text=BUTTONS["see_polls"]),
        KeyboardButton(text=BUTTONS["admin_btc_banker"]),
    ],
    [
        KeyboardButton(text=BUTTONS["admin_panel_ban"]),
        KeyboardButton(text=BUTTONS["add_admin"]),
        KeyboardButton(text=BUTTONS["add_moder"]),
        KeyboardButton(text=BUTTONS["admin_check_payments"])
    ],
    find_employees_menu.keyboard[0]
]
                                 )

# ==== Moderator menu ==== #
moder_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS["see_polls"]),
    ],
    find_employees_menu.keyboard[0]
]
                                 )

# ============================= POLL ==================================== #
# ==== Start pool menu ==== #
start_poll_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['poll_get_ready']),
    ]
])

# ==== Re_send menu ==== #
re_send_poll = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['re_send_poll']),
        KeyboardButton(text=BUTTONS['btn_back']),
    ]
])

# ==== POLL:COLOR ==== #
poll_color_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['pcolor_white']),
        KeyboardButton(text=BUTTONS['pcolor_gray']),
        KeyboardButton(text=BUTTONS['pcolor_black']),
    ],
    back_cancel_menu.keyboard[0]
])

# ==== POLL:DIFFICULTY ==== #
poll_diff_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text='1️⃣'),
        KeyboardButton(text='2️⃣'),
        KeyboardButton(text='3️⃣'),
        KeyboardButton(text='4️⃣'),
        KeyboardButton(text='5️⃣'),
    ],
    [
        KeyboardButton(text='6️⃣'),
        KeyboardButton(text='7️⃣'),
        KeyboardButton(text='8️⃣'),
        KeyboardButton(text='9️⃣'),
        KeyboardButton(text='🔟'),
    ],
    back_cancel_menu.keyboard[0]
])


# ==== POLL:CONFIRM ==== #
def poll_contact_menu(username: str):
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
        [
            KeyboardButton(text=f'@{username}'),
        ],
        back_cancel_menu.keyboard[0]
    ])


# ==== POLL:CONFIRM ==== #
poll_confirm_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['pconfirm_next']),
    ],
    [
        KeyboardButton(text=BUTTONS['pconfirm_again']),
    ],
    [
        KeyboardButton(text=BUTTONS['btn_back']),
    ]
])

# ==== POLL:SUBSCRIPTION TYPE ==== #
poll_subs_type = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['sub_type_1']),
        KeyboardButton(text=BUTTONS['sub_type_2']),
    ],
    back_cancel_menu.keyboard[0]
]
                                     )

# ==== POLL:SUBSCRIPTION LENGTH ==== #
poll_subs_length = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=[
    [
        KeyboardButton(text='3 дня'),
    ],
    [
        KeyboardButton(text='7 дней'),
    ],
    [
        KeyboardButton(text='30 дней'),
    ],
    back_cancel_menu.keyboard[0]
]
                                       )

# ============================= PROFILE ==================================== #
profile_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text=BUTTONS['profile_back']),
    ]
])
