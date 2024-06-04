from telebot.types import InlineKeyboardButton, ChatMemberLeft
from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.database.models.users import Authors, Stats
from MODULES.database.models.boost_channels import BoostChannels


class Boost:
    def __init__(self, user: Authors):
        self.db_user = user

    @property
    def amount(self) -> int:
        data = map(lambda x: x.amount if not isinstance(
            GUARD.get_chat_member(chat_id=x.tid, user_id=self.db_user.tg_id),
            ChatMemberLeft
        ) else 0, BoostChannels.select())

        return sum(data)

    @property
    def chn_buttons(self) -> list[InlineKeyboardButton]:
        data = list(filter(lambda x: isinstance(GUARD.get_chat_member(chat_id=x.tid, user_id=self.db_user.tg_id), ChatMemberLeft), BoostChannels.select()))
        data = list(map(lambda x: InlineKeyboardButton(f'Канал {x.id} (+{x.amount} рейтинга)', url=x.link), data))

        return data

    def rollback(self):
        self.db_user.stat.total_boost = self.amount
        Stats.save(self.db_user.stat)

    @property
    def boost_changed(self) -> int:
        return self.db_user.stat.total_boost - self.amount
