from loader import bot
from src.data.config import MIN_DESCRIPT_LEN, MIN_CONTACT_LEN


async def validate_poll_color(text):
    return text in ['▫️Белая▫️', '▪️Черная▪️', '⛓Серая⛓']


async def validate_poll_difficulty(text):
    return text in '1 2 3 4 5 6 7 8 9 10 1️⃣ 2️⃣ 3️⃣ 4️⃣ 5️⃣ 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟'.split()


async def validate_poll_contact(text):
    try:
        return text[0] == '@' and len(text) >= MIN_CONTACT_LEN and not any([x in text for x in ' !#$%^&*;:,'])
    except:
        return False

async def validate_poll_description(text):
    return len(text) >= MIN_DESCRIPT_LEN


def validate_poll_post_time(text: str, sub_type: int):
    try:
        splitted = text.replace(' ', ':').split(':')
        hours1 = splitted[0].zfill(2)
        minutes1 = splitted[1].zfill(2)
        if len(hours1) != 2 or len(minutes1) != 2:
            return False
        if sub_type == 2:
            hours2 = splitted[2].zfill(2)
            minutes2 = splitted[3].zfill(2)
            if len(hours2) != 2 or len(minutes2) != 2:
                return False
            return f'{hours1}:{minutes1} {hours2}:{minutes2}' if 0 <= int(hours1) <= 23 and \
                                                                             0 <= int(minutes1) <= 59 and \
                                                                             0 <= int(hours2) <= 23 and \
                                                                             0 <= int(minutes2) <= 59 and \
                                                                             1 <= len(hours1) <= 2 and \
                                                                             1 <= len(hours2) <= 2 and \
                                                                             len(minutes1) == len(minutes2) == 2 \
                else False
        else:
            return f'{hours1}:{minutes1}' if 0 <= int(hours1) <= 23 and \
                                                     0 <= int(minutes1) <= 59 and \
                                                     1 <= len(hours1) <= 2 and \
                                                     len(minutes1) == 2 \
                else False
    except:
        return False
