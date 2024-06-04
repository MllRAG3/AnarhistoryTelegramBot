import time
import schedule

from telebot.types import Message, InlineKeyboardMarkup
from MODULES.database.models.mailing import Mailing
from MODULES.database.models.users import Authors
import MODULES.domain.user_request_executors.util as ure_util


class MailingSender:
    def __init__(self, message: Message):
        self.message: Message = message
        self.work: bool = True

    def schedule_send(self):
        for msg in Mailing.select():
            schedule.every().day.at(str(msg.send_time)).do(self.send, msg.id).tag(str(msg.id))

    @staticmethod
    def send(id_):
        mailing: Mailing = Mailing.get_by_id(id_)
        for uid in map(lambda x: x.chat_id, Authors.select()):
            ure_util.send(
                type=mailing.type,
                kwargs_json=mailing.message_json,
                markup=InlineKeyboardMarkup.de_json(mailing.buttons_json),
                chat_id=uid
            )
        schedule.clear(str(id_))

    def restart(self):
        self.work = False
        time.sleep(1)
        self()

    def __call__(self):
        self.schedule_send()
        while self.work:
            schedule.run_pending()
