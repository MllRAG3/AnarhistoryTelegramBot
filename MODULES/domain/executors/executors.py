from telebot.types import InlineKeyboardButton, Message, User

import time
import random

from MODULES.constants.reg_variables.BOT import GUARD
from MODULES.constants.reg_variables.MORPH import MORPH


from MODULES.domain.pre_send.call_data_handler import Call
from MODULES.domain.pre_send.page_compiler import PageLoader
from MODULES.domain.pre_send.page_message.page_message import PageSwitcher
from MODULES.domain.pre_send.graph_loader import GraphLoader

import MODULES.database.models.users as ussr
import MODULES.database.models.user_history as uh

import MODULES.constants.reg_variables.PAGE_MESSAGE as PM
PAGE_MESSAGE = PM.PAGE_MESSAGE


def button(text, call_data) -> InlineKeyboardButton:
    return InlineKeyboardButton(text, callback_data=call_data)


def log(func):
    def inner(self, *args, **kwargs):
        uh.UserHistory.create(page_name=func.__name__, user=self.db_user)
        func(*args, **kwargs)

    return inner


def authors_only(func):
    def inner(self, *args, **kwargs):
        if not self.db_user.is_author:
            uh.UserHistory.create(page_name=func.__name__, user=self.db_user)
            self.edit(PageLoader(4)().to_dict)
            return
        func(*args, **kwargs)

    return inner


class BaseExec(Call):
    def __init__(self, message: Message, user: User | None = None):
        self.message: Message = message
        self.user = message.from_user if user is None else user

        self.db_user = None
        self.load_db_user()

    def load_db_user(self):
        try:
            self.db_user = ussr.Users.get(tg_id=self.user.id)
        except Exception as e:
            err = e
            ser_pref = ussr.SearchPreferensies.create()
            anon_sett = ussr.AnonymousSettings.create()
            data = {
                'username': self.user.username,
                'tg_id': self.user.id,
                'search': ser_pref,
                'anonymous': anon_sett
            }
            self.db_user: ussr.Users = ussr.Users.create(**data)

    def send(self, data: dict):
        GUARD.send_message(chat_id=self.message.chat.id, **data)

    def edit(self, data: dict):
        GUARD.edit_message_text(chat_id=self.message.chat.id, message_id=self.message.id, **data)

    @staticmethod
    def change_page(delta):
        if not PAGE_MESSAGE:
            return
        PAGE_MESSAGE.change_page(delta)

    def back(self):
        last = uh.UserHistory.select().order_by(uh.UserHistory.created_at.desc())[-1].page_name
        uh.UserHistory.delete_by_id(last.id)
        obj = getattr(self, last)
        obj()

    def cancel(self):
        GUARD.clear_step_handler(self.message)
        self.back()


class FirstMessages(BaseExec):
    def start(self):
        pg = PageLoader(1)()
        self.send(pg.to_dict)

    def rules(self):
        pld = PageLoader(2)
        for second in range(10, -1, -1):
            self.edit(pld(f"{second} сек.").to_dict)
            time.sleep(1)
        pld += [button(">>-ДАЛЬШЕ->", 'main')]
        self.edit(pld("можно переходить дальше:]").to_dict)


class Main(BaseExec):
    def main(self):
        pld = PageLoader(3)
        if not self.db_user.is_author:
            pld += [button('>>Стать автором>> БЕЗ ЭТОГО НИКАК', 'become_an_author')]
        self.edit(pld().to_dict)


class Help(BaseExec):
    pass


class Settings(BaseExec):
    def become_an_author(self):
        self.edit(PageLoader(6)().to_dict)
        GUARD.register_next_step_handler(self.message, self.check_author_name, 9, True, True, True)

    def check_author_name(self, message, success_id, *success_settings):
        other = ussr.Users.select().where(ussr.Users.author_name == message.text)[:]
        if other:
            self.edit(PageLoader(7)().to_dict)
        self.edit(PageLoader(8)(message.text).to_dict)
        time.sleep(3)
        self.edit(PageLoader(success_id, *success_settings)().to_dict)

    @log
    @authors_only
    def settings_main(self):
        self.edit(PageLoader(5, False, True, True)().to_dict)

    @log
    @authors_only
    def change_anonymous_pref(self):
        pld = PageLoader(10, True, True, True)
        pld += [button("Посты и профиль: {}".format('АНОНИМНО' if self.db_user.anonymous.profile else 'НЕ АНОНИМНО'), "change_anon_posts {}".format(int(not self.db_user.anonymous.profile)))]
        pld += [button("Подписки: {}".format('АНОНИМНО' if self.db_user.anonymous.subscriptions else 'НЕ АНОНИМНО'), "change_anon_subs {}".format(int(not self.db_user.anonymous.subscriptions)))]
        self.edit(PageLoader(10, True, True, True)().to_dict)

    def change_anon_posts(self, value):
        self.db_user.anonymous.profile = bool(int(value))
        ussr.Users.save(self.db_user)

    def change_anon_subs(self, value):
        self.db_user.anonymous.subscriptions = bool(int(value))
        ussr.Users.save(self.db_user)

    @log
    @authors_only
    def change_author_name(self):
        self.edit(PageLoader(11, True, True, True)(self.db_user.author_name).to_dict)

    def reg_author_name(self):
        self.edit(PageLoader(12)().to_dict)
        GUARD.register_next_step_handler(self.message, self.check_author_name, 5, True, True, True)

    @log
    @authors_only
    def change_search_prefs(self):
        pld = PageLoader(13, True, True, True)
        authors = self.db_user.search.show_authors
        row = [button("Авторы: {}".format("ДА" if authors else "НЕТ"), '...')]
        if authors:
            row.extend([
                button('-1', '...'),
                button('+1', '...')
            ])
        pld += row

        stories_by_head = self.db_user.search.show_stories_by_title
        row = [button("Истории по заглавию: {}".format("ДА" if stories_by_head else "НЕТ"), '...')]
        if stories_by_head:
            row.extend([
                button('-1', '...'),
                button('+1', '...')
            ])
        pld += row

        stories_by_text = self.db_user.search.show_stories_by_text
        row = [button("Истории по тексту {}:".format("ДА" if stories_by_text else "НЕТ"), '...')]
        if stories_by_text:
            row.extend([
                button('-1', '...'),
                button('+1', '...')
            ])
        pld += row

        self.edit(pld(
            self.db_user.search.show_authors_n,
            self.db_user.search.show_stories_by_title_n,
            self.db_user.search.show_stories_by_text_n
        ).to_dict)

    def change_search(self, name, delta):
        pass
