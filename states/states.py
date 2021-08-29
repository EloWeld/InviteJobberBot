from aiogram.dispatcher.filters.state import StatesGroup, State


class EmployeesPoll(StatesGroup):
    Color = State()
    Difficulty = State()
    Wages = State()
    Time = State()
    Description = State()
    Contact = State()
    Confirm = State()
    SubscriptionType = State()
    SubscriptionLength = State()
    PostingTime = State()
    Payment = State()


class RejectState(StatesGroup):
    Reason = State()


class AdminState(StatesGroup):
    Ban = State()
    Username = State()
    Changes = State()
    Admin = State()
    Moder = State()


