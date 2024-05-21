from MODULES.constants.config import MAIN_BOT_TOKEN

from typing import Final
from telebot import TeleBot


GUARD: Final[TeleBot] = TeleBot(MAIN_BOT_TOKEN)
