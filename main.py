from telebot.types import Message, CallbackQuery, InlineQuery
from telebot.util import extract_arguments

from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.database.util.create_tables import create_world
from MODULES.domain.ads_executors.to_json import ToJson
from MODULES.domain.user_request_executors.executors import Exec, Search
from MODULES.database.models.users import Authors


@GUARD.message_handler(commands=["start", "main"])
def start(message: Message):
    Exec(message).start()


@GUARD.message_handler(commands=['at_story'])
def at_story(message):
    GUARD.delete_message(message.chat.id, message.id)
    Exec(message).at_story(int(extract_arguments(message.text)))


@GUARD.message_handler(commands=['dismember'])
def for_ads(message: Message):
    user: Authors = Authors.get_or_none(tg_id=message.from_user.id)
    if user is None:
        return
    if not user.is_admin:
        return
    GUARD.send_message(message.chat.id, 'Перешли сюда рекламный пост и я расчленю его для бд:')
    tj = ToJson()
    GUARD.register_next_step_handler(message, callback=tj)
    while not tj.is_called:
        pass
    GUARD.send_message(message.chat.id, str(tj), parse_mode='HTML')



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
