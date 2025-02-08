import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GROUP_CHAT_ID = os.getenv("GROUP_CHAT_ID")
PRESENCE_CHECK_START = os.getenv("PRESENCE_CHECK_START")
PRESENCE_CHECK_END = os.getenv("PRESENCE_CHECK_END")
PRESENCE_REPORT = (os.getenv("PRESENCE_REPORT").strip('[]')
                   .replace('"', '').split(', '))
PRESENCE_REPORT_LOG = os.getenv("PRESENCE_REPORT_LOG")
DATE_FIRST_LESSON = os.getenv("DATE_FIRST_LESSON")

FILENAME_LOG = "log.txt"