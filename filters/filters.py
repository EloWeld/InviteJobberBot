from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from src.data.config import superadmin
from src.data.database import UsersDB


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        member = str(message.from_user.id) == superadmin
        member = member or UsersDB.get_0user_data(message.from_user.id, 'privilege') == 'admin'
        return member


class IsModerator(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        member = UsersDB.get_0user_data(message.from_user.id, 'privilege') in ['moder', 'admin']
        return member


class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE


class IsGroup(BoundFilter):
    async def check(self, message: types.Message, *args) -> bool:
        return message.chat.type in [
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
            types.ChatType.SUPER_GROUP,
        ]