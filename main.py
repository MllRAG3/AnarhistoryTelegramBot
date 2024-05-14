from telebot.types import Message, CallbackQuery, InlineQuery

from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.database.util.create_tables import create_world
from MODULES.domain.executors.executors import FirstMessages, Main

import MODULES.constants.reg_variables.PAGE_MESSAGE as PM
PAGE_MESSAGE = PM.PAGE_MESSAGE


@GUARD.message_handler(commands=["start"])
def start(message: Message):
    ex = FirstMessages(message)
    ex.start()


@GUARD.callback_query_handler(func=lambda call: True)
def call_data_handler(call: CallbackQuery):
    FirstMessages(call.message, user=call.from_user)(call)
    Main(call.message, user=call.from_user)(call)


@GUARD.inline_handler(func=lambda query: True)
def inline_handler(inline_query: InlineQuery):
    pass


if __name__ == "__main__":
    create_world()
    GUARD.infinity_polling(skip_pending=True)
