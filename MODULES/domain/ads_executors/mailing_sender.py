import schedule

from MODULES.database.models.mailing import Mailing
from MODULES.database.models.users import Authors


class MailingSender:
    def __init__(self, message):
        self.message = message

    def schedule_send(self):
        for msg in Mailing.select():
            schedule.every().day.at(str(msg.send_time)).do(self.send, msg.id).tag(str(msg.id))

    def send(self, id_):
        for uid in map(lambda x: x.chat_id, Authors.select()):
            pass

    def __call__(self):
        pass
