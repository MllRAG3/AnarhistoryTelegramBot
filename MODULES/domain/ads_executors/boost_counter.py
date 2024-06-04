from telebot.types import ChatMember, ChatMemberMember
from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.database.models.users import Authors
from MODULES.database.models.boost_channels import BoostChannels


class Boost:
    def __init__(self, user: Authors):
        self.db_user = user

    @property
    def amount(self) -> list[int]:
        data = map(lambda x: x.amount if isinstance(
            GUARD.get_chat_member(chat_id=x.tid, user_id=self.db_user.tg_id),
            ChatMemberMember
        ) else 0, BoostChannels.select())
        data = list(filter(lambda x: x != 0, data))

        return sum(data)

    @property
    def not_sub_channel_links(self) -> list[BoostChannels]:
        data = list(filter(lambda x: not isinstance(GUARD.get_chat_member(chat_id=x.tid, user_id=self.db_user.tg_id), ChatMemberMember), BoostChannels.select()))

        return data

    @property
    def boost_changed(self) -> bool:
        return self.db_user.stat.total_boost != self.amount
