from loader import bot
from src import PollDB
from src.data.config import PollStatus, MESSAGES
from utils.helpers import *


async def inavtive_poll(poll_entity: dict):
    PollDB.update_poll_field(poll_entity["id"], 'status', str(PollStatus.INACTIVE))
    await bot.send_message(poll_entity['owner_id'],
                           text=MESSAGES["autoposting_stopped"])


async def publish_poll(poll_id: str):
    poll_entity = PollDB.polls_filter('id', str(poll_id))[0]

    # Обновляем записи в бд
    PollDB.update_poll_field(poll_id, 'pub_time', get_current_datetime())
    PollDB.update_poll_field(poll_id, 'status', str(PollStatus.ACTIVE))

    await bot.send_message(poll_entity['owner_id'],
                           text=MESSAGES["your_vacancy_approved"].format(poll_id))


async def reject_poll(poll_id: str, mod_username: str, reason: str):
    poll_owner_id = PollDB.polls_filter('id', poll_id)[0]["owner_id"]
    # Обновляе запись в бд
    PollDB.update_poll_field(poll_id, 'status', PollStatus.INACTIVE)

    await bot.send_message(poll_owner_id,
                           text=MESSAGES["your_vacancy_rejected"].format(poll_id, mod_username))
    await bot.send_message(poll_owner_id,
                           text=reason)