from datetime import datetime
from .config import PRESENCE_CHECK_START, PRESENCE_CHECK_END

def is_current_time_in_range():
    current_time = datetime.now().strftime("%H:%M")

    return PRESENCE_CHECK_START <= current_time < PRESENCE_CHECK_END

class FlagRegistration:
    def __init__(self):
        self.flag = False

    def set(self, state):
        self.flag = state

    def get(self):
        return self.flag
