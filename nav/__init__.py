from src import UsersDB
from .inline_markups import *
from .reply_markups import *
from .tabs import *


def get_user_menu(user_id):
    user_lvl = UsersDB.get_0user_data(user_id, 'privilege')
    if user_lvl == 'admin':
        return admin_menu
    elif user_lvl == 'moderator':
        return moder_menu
    else:
        return find_employees_menu
