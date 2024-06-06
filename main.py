from telebot.types import Message, CallbackQuery, InlineQuery
from telebot.util import extract_arguments

from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.database.util.create_tables import create_world
from MODULES.domain.user_request_executors.executors import BotPages, Search
from MODULES.domain.ads_executors.mailing_sender import MailingSender


@GUARD.message_handler(commands=["start", "main"])
def start(message: Message):
    executor = BotPages(message)
    executor.start()
    executor.check_boosts()


@GUARD.message_handler(commands=['at_story'])
def at_story(message):
    executor = BotPages(message)
    executor.at_story(int(extract_arguments(message.text)))


@GUARD.message_handler(commands=['dismember'])
def for_ads(message: Message):
    executor = BotPages(message)
    executor.dismember_message()


@GUARD.message_handler(commands=['no_command'])
def rickroll(message: Message):
    executor = BotPages(message)
    executor.rickroll()


@GUARD.message_handler(commands=['start_mailing_28374823974'])
def start_mailing(message: Message):
    MailingSender()()


@GUARD.message_handler(func=lambda message: message.text == '<-НАЗАД-<<')
def main(message: Message):
    executor = BotPages(message)
    executor.show_story(story=executor.previous_story)


@GUARD.message_handler(func=lambda message: message.text == 'ГЛАВНАЯ')
def main(message: Message):
    executor = BotPages(message)
    executor.main()


@GUARD.message_handler(func=lambda message: message.text == '>>-ДАЛЬШЕ->')
def main(message: Message):
    executor = BotPages(message)
    executor.show_story(story=executor.next_story)


@GUARD.message_handler(func=lambda message: 'ОТБЛАГОДАРИТЬ' in message.text)
def main(message: Message):
    executor = BotPages(message)
    executor.respect(1, message.text.strip('ОТБЛАГОДАРИТЬ').strip())


@GUARD.callback_query_handler(func=lambda call: True)
def call_data_handler(call: CallbackQuery):
    executor = BotPages(call.message, user=call.from_user)
    executor(call)
    executor.check_boosts()


@GUARD.inline_handler(func=lambda query: True)
def inline_handler(inline_query: InlineQuery):
    Search(inline_query).search()


@GUARD.message_handler(content_types=['text'])
def delete_trash(message):
    GUARD.delete_message(message.chat.id, message.id)


if __name__ == "__main__":
    create_world()
    GUARD.infinity_polling(skip_pending=True)
