import asyncio

from loader import bot
from main.poll_controller import inavtive_poll
from main.posting import post_timer_callback
from src import PollDB, UsersDB, CheckDB
from src.data.config import JOBS_CHAT_ID, PollStatus, MESSAGES, BOT_REFRESH_RATE
from utils.helpers import get_current_time, get_subscription_diff
import nest_asyncio


def asyncio_run(future, as_task=True):
    """
    A better implementation of `asyncio.run`.

    :param future: A future or task or call of an async method.
    :param as_task: Forces the future to be scheduled as task (needed for e.g. aiohttp).
    """

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # no event loop running:
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(_to_task(future, as_task, loop))
    else:
        nest_asyncio.apply(loop)
        return asyncio.run(_to_task(future, as_task, loop))


def _to_task(future, as_task, loop):
    if not as_task or isinstance(future, asyncio.Task):
        return future
    return loop.create_task(future)


minute_vacancies = []
days_vacancies = []


# Обрабатываем отправку постов в другом потоке с таймером
def posting_startup():
    loop_bot = asyncio.get_event_loop()
    loop_bot.create_task(scheduled(BOT_REFRESH_RATE, post_timer_callback))

    loop_minutes = asyncio.get_event_loop()
    loop_minutes.create_task(scheduled(62, minutes_timer_callback))

    loop_days = asyncio.get_event_loop()
    loop_days.create_task(scheduled(61 * 60 * 24, days_timer_callback))

    loop_hours = asyncio.get_event_loop()
    loop_hours.create_task(scheduled(61 * 60, hours_timer_callback))


async def scheduled(wait_for, func):
    while True:
        await asyncio.sleep(wait_for)
        await func()


async def minutes_timer_callback():
    global minute_vacancies
    minute_vacancies = []

    # Check checks db
    checks = CheckDB.all_checks()
    admins = UsersDB.filter('privilege', 'admin')
    if len(checks) > 0:
        for admin in admins:
            await bot.send_message(chat_id=admin["id"],
                                   text=f'‼ Есть новые чеки от банкира({len(checks)}) ‼ Обработайте их в меню /banker')


async def days_timer_callback():
    global days_vacancies
    days_vacancies = []


async def hours_timer_callback():
    moderation_polls = PollDB.polls_filter('status', str(PollStatus.ON_MODERATION))
    admins = UsersDB.filter('privilege', 'admin')
    moderators = UsersDB.filter('privilege', 'moderator')
    if len(moderation_polls) != 0:
        for admin in admins:
            await bot.send_message(chat_id=admin["id"],
                                   text='‼ Есть новые анкеты на модерации ‼ Обработайте их в меню /polls')
        for moder in moderators:
            await bot.send_message(chat_id=moder["id"],
                                   text='‼ Есть новые анкеты на модерации ‼ Обработайте их в меню /polls')
