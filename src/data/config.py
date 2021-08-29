import enum
import os

from dotenv import load_dotenv
from glQiwiApi import QiwiWrapper

load_dotenv()
# ===== BOT ===== #
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_NAME = os.getenv('BOT_NAME')
BOT_DESC = os.getenv('BOT_DESC')
superadmin = os.getenv("WELOXD_ID")
PROFILE_GIF_FILEID = 'CgACAgIAAxkBAAIO1WEniaPKVj67ROYRpynvv1nmtoXLAAJyDwACSmM4SUPGbw-JZDSvIAQ'
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT

# ===== QIWI ===== #
QIWI_PHONE_NUMBER = os.getenv('QIWI_PHONE_NUMBER')
QIWI_TOKEN = os.getenv('QIWI_TOKEN')
QIWI_P2P = os.getenv('QIWI_P2P')
QIWI_SECRET = os.getenv('QIWI_SECRET')

# ===== YOOMONEY ===== #
YOOMONEY_CLIENT_ID = os.getenv('YOOMONEY_CLIENT_ID')
YOOMONEY_SECRET = os.getenv('YOOMONEY_SECRET')
YOOMONEY_REDIR = os.getenv("YOOMONEY_REDIR")
YOOMONEY = os.getenv("YOOMONEY")
YOOMONEY_ACCESS_TOKEN = os.getenv("YOOMONEY_ACCESS_TOKEN")

# ===== BTC BANKER ===== #
BTC_BANKER_WALLET = os.getenv('BTC_BANKER_WALLET')

# ===== CHAT ===== #
JOBS_CHAT_ID = os.getenv('CHAT_ID')
CHAT_LINK = os.getenv('CHAT_LINK')

# ===== POLL ===== #
# Please don't set it lose than 60 second! You can get fatal error and bot will be shot downed!
BOT_REFRESH_RATE = 15

# ========== PAYMENT ======= #
QIWI_WALLET = QiwiWrapper(
    phone_number=QIWI_PHONE_NUMBER if QIWI_PHONE_NUMBER[0] == '+' else f'+{QIWI_PHONE_NUMBER}',
    api_access_token=QIWI_TOKEN,
    secret_p2p=QIWI_SECRET,
    without_context=True
)

# ========== POLL ========== #
class PollStatus(enum.Enum):
    INACTIVE = 0
    ACTIVE = 1
    EDITING = 2
    ON_MODERATION = 3
    PAYMENT = 3


MIN_CONTACT_LEN = 1
MIN_DESCRIPT_LEN = 1
REPLACES = {
    '▫️Белая▫️': 'Белая',
    '⛓Серая⛓': 'Серая',
    '▪️Черная▪️': 'Черная',

    '1️⃣': 1,
    '2️⃣': 2,
    '3️⃣': 3,
    '4️⃣': 4,
    '5️⃣': 5,
    '6️⃣': 6,
    '7️⃣': 7,
    '8️⃣': 8,
    '9️⃣': 9,
    '🔟': 10,

    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,

    '3 дня': 3,
    '7 дней': 7,
    '30 дней': 30,
}
PRICE_COLOR_MULTIPLY = {
    'Белая': 1,
    'Серая': 2.5,
    'Черная': 8,
}
PRICELIST = {
    1: {
        3: 2, # 150
        7: 2, # 250
        30: 2, # 800
    },
    2: {
        3: 250, # 250
        7: 400, # 400
        30: 1500, # 1500
    }
}

MESSAGES = {
    'autoposting_stopped': '❗️Автопостинг приостановлен. Продлить его можно в меню "Профиль".',
    'your_vacancy_approved': '🌀Ваша анкета #{} одобрена модератором и выставлена в чате, Поздравляем!🌀',
    'your_vacancy_rejected': 'Ваша анкета {} была модератором {} отклонена по причине: ',
    'bot_statistics':
'''
💫💫💫💫💫💫💫💫
    Статистика бота:

• Юзеров: {}
• Общий депозит юзеров: {}
• Активных подписок: {}
• Подписок требующих модерации: {}

💫💫💫💫💫💫💫💫
''',
    'bot_moto':
'''
🎩 Добро пожаловать, <b>{}</b>! 

 🤖<b>Для чего этот бот:</b>
   ├ Создание рекламного поста.
   ├ <b>🔥Автопостинг в чат.</b>
   └ Оплата подписки.

<b>Благодаря боту</b> вы сможете в кратчайшие сроки <b><u>найти работников</u></b>.

⏱<b>Вам не придётся публиковать свой пост</b>, наш Бот сделает это за вас.
''',
    'poll_moto':
'''
            🛸Если вы желаете размещаться в моем чате и найти работников, то вам нужно будет заполнить анкету:
        
        
        1) <b>Цвет работы.</b>
        2) <b>Сложность.</b>
        3) <b>Зарплата.</b>
        4) <b>Время работы.</b>
        5) <b>Описание.</b>
        6) <b>Связь.</b>
        
        Далее наш алгоритм сформирует из полученной информации Ваш рекламный пост и Вы сможете размещать рекламу в чате.
''',
    'vacancy_preview':
'''
#ищуработников

<b>Цвет работы:</b> {}
<b>Сложность:</b> {}
<b>Заработная плата:</b> {} 
<b>Время работы:</b> {}
<b>Описание:</b> {}

<b>📝 Связь:</b> {}
<b>🎩 Гарант:</b> @scrooge_garantbot
''',
    'bot_no_vacancy': '❗ Вы не оформляли анкету, исправить это можно в главном меню или командой /find_employs\n',
    'bot_start_msg': 'Бот <b><u>{}</u></b> запущен в {}',
    'poll_color_lbl': '1️⃣ Цвет работы: ',
    'poll_difficulty_lbl': '2️⃣ Сложность работы: ',
    'poll_wages_lbl': '3️⃣ Зарплата: ',
    'poll_time_lbl': '4️⃣ Время работы: ',
    'poll_desc_lbl': '5️⃣ Распишите описание работы как можно подробнее:',
    'poll__lbl': '',
    'unknow_cmd': '❓ Неизвестная команда ❔',
    'invalid_input': '💢 Некорректный ввод, попробуйте ещё раз! 💢',
    'unknown_db_user': '💢 Такого пользователя нет в БД! 💢',
    'new_admin_username': '👑 Введите @username нового админа',
    'new_moder_username': '👑 Введите @username нового модератора',
    'ban_username': 'Введите точный username в формате @username чтобы забанить пользователя',
    'moder_notify_sender': '🖤 Поздравляем, юзер @{} теперь стал модератором',
    'moder_notify': '🖤 Поздравляем, теперь вы стали модератором! Вас назначил @{}',
    'admin_notify_sender': '👑 Поздравляем, юзер @{} теперь стал админом 👑',
    'admin_notify': '👑 Поздравляем, теперь вы стали админом! Вас назначил @{}',
    'sub_expires_1day': '⭕️Ваша подписка истекает завтра, советуем вам её продлить!',
    'sub_type_moto': 'Хорошо, давай определимся с типом подписки, на данный момент у нас есть два типа:\n' +
                             '<b>• Обычная подписка (1 раз в день)</b>\n' +
                             '<b>• Премиум подписка (2 раз в день)</b>\n',
}

BUTTONS = {
    'start': '⭐ Начать ⭐',
    're_send_poll': 'Перехаполнить анкету',
    'poll_get_ready': '☕️Приступить',
    'next': '✅ Всё ОК, едем дальше ✅',
    'pcolor_white': '▫️Белая▫️',
    'pcolor_gray': '⛓Серая⛓',
    'pcolor_black': '▪️Черная▪️',
    'pconfirm_next': '👌 Всё верно, продолжаем 👌',
    'pconfirm_again': '❌ Нет, я заполню анкету заново ❌',
    'sub_type_1': '🔎 Обычная',
    'sub_type_2': '🎖 Premium',

    'admin_panel_magic': '🧙‍♀️ Изменить подписку юзера 🧙‍♂️',
    'admin_panel_ban': '🚫 Забанить юзера 🚫',
    'statistics': '🧷 Статистика 🎩',
    'add_admin': '👑 Добавить админа 👑',
    'add_moder': '😎 Добавить модератора 😎',
    'admin_check_payments': '💲 Панель платежей 💲',
    'admin_btc_banker': '🏦 BTC Банкир 🏦',

    'see_polls': '🔍 Посмотреть заявки на модерацию',

    'find_employs': '🔍 Найти работников',
    'chat': '📨 Чат',
    'profile': '🎩 Профиль',

    'profile_my_poll': '☕ Моя анкета',
    'profile_back': '🔙 Назад',
    'chat_link': '↗ Перейти в чат ↗',

    'btn_back': '⬅ Назад',
    'btn_cancel': '🚫 Отмена'
}

DECODE_POLL = {
    'sub_type': {
        '1': 'Обычная',
        '2': 'Премиум'
    },
    'status': {
        'PollStatus.EDITING': 'Редактируется',
        'PollStatus.ACTIVE': 'Активна',
        'PollStatus.PAYMENT': 'Оплачивается',
        'PollStatus.INACTIVE': 'Неактивна',
        'PollStatus.ON_MODERATION': 'На проверке',
    }
}

minute_vacancies = []
days_vacancies = []