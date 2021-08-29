import asyncio

from loader import bot
from main.poll_controller import inavtive_poll
from src import PollDB, UsersDB
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



async def post_timer_callback():
    global days_vacancies
    global minute_vacancies
    # FORMAT WARNING!
    polls = PollDB.polls_filter('status', str(PollStatus.ACTIVE))
    for poll_ent in polls:
        # Вычисляем разницу между текущим временем и временем оформления подписки
        date_diff_days = get_subscription_diff(poll_ent['pub_time'])[0]
        # Срок действия анкеты истёк!
        if date_diff_days > int(poll_ent['sub_len']):
            await inavtive_poll(poll_ent)

        # До конца срока 1 день!
        if date_diff_days == int(poll_ent['sub_len']) and poll_ent['owner_id'] not in days_vacancies:
            await bot.send_message(chat_id=poll_ent['owner_id'],
                                   text=MESSAGES["sub_expires_1day"])
            days_vacancies += poll_ent['owner_id']

        # Проверяем, пришло ли время публикации для анкеты
        time = get_current_time('%H:%M')
        times = poll_ent["posting_time"].split(' ')
        if time in times and poll_ent['vacancy'] not in minute_vacancies:
            await bot.send_message(chat_id=JOBS_CHAT_ID,
                                   text=poll_ent['vacancy'])
            minute_vacancies += [poll_ent['vacancy']]
