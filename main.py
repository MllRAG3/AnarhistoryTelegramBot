from telebot.types import Message, CallbackQuery, InlineQuery
from telebot.util import extract_arguments

from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.database.util.create_tables import create_world
from MODULES.domain.user_request_executors.executors import Exec, Search
from MODULES.domain.ads_executors.mailing_sender import MailingSender


@GUARD.message_handler(commands=["start", "main"])
def start(message: Message):
    Exec(message).start()


@GUARD.message_handler(commands=['at_story'])
def at_story(message):
    GUARD.delete_message(message.chat.id, message.id)
    Exec(message).at_story(int(extract_arguments(message.text)))


@GUARD.message_handler(commands=['dismember'])
def for_ads(message: Message):
    Exec(message).dismember_message()


@GUARD.message_handler(commands=['no_command'])
def rickroll(message: Message):
    Exec(message).rickroll()


@GUARD.message_handler(commands=['start_mailing_28374823974'])
def start_mailing(message: Message):
    MailingSender()()


@GUARD.callback_query_handler(func=lambda call: True)
def call_data_handler(call: CallbackQuery):
    Exec(call.message, user=call.from_user)(call)


@GUARD.inline_handler(func=lambda query: True)
def inline_handler(inline_query: InlineQuery):
    Search(inline_query).search()


@GUARD.message_handler(content_types=['text'])
def delete_trash(message):
    GUARD.delete_message(message.chat.id, message.id)


if __name__ == "__main__":
    create_world()
    GUARD.infinity_polling(skip_pending=True)
