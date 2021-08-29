from threading import Timer

from loader import bot
from src.data.config import MIN_DESCRIPT_LEN, MIN_CONTACT_LEN


class PostingTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)
