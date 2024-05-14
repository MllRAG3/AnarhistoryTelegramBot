from MODULES.domain.pre_send.page_compiler import PageLoader
from MODULES.domain.pre_send.page_message.cursor import Cursor
from MODULES.domain.pre_send.call_data_handler import Call
from MODULES.constants.reg_variables.BOT import GUARD
from telebot.types import InlineKeyboardButton, Message

from math import ceil


class PageSwitcher(Call):
    def __init__(self, message: Message, page_id: int, buttons: list[InlineKeyboardButton], buttons_on_page=5):
        self.message: Message = message
        self.page_id: int = page_id
        self.buttons: list[InlineKeyboardButton] = buttons
        self.buttons_on_page: int = buttons_on_page
        self.cur = Cursor(ceil(len(buttons) / buttons_on_page))

        self.page = 0
        self.update()

    def change_page(self, delta: int | str):
        if type(delta) is str:
            delta = int(delta)

        self.page = int(abs(self.page + delta) % (len(self.buttons) / self.buttons_on_page))
        self.cur += delta
        self.update()

    @property
    def page_buttons(self):
        start, end = self.page * self.buttons_on_page, (self.page + 1) * self.buttons_on_page
        return self.buttons[start:end]

    @property
    def navigation_buttons(self):
        if len(self.buttons) > self.buttons_on_page:
            back_b, next_b = InlineKeyboardButton('<-пред. стр.-<<', callback_data='change_page -1'), InlineKeyboardButton('>>-след. стр.->', callback_data='change_page 1')
            return [back_b, InlineKeyboardButton('На главную', callback_data='main'), next_b]
        return [InlineKeyboardButton('На главную', callback_data='main')]

    def update(self):
        loader: PageLoader = PageLoader(self.page_id)
        loader += self.page_buttons
        loader += self.navigation_buttons

        pg = loader()
        GUARD.edit_message_text(chat_id=self.message.chat.id, message_id=self.message.id, **pg.to_dict)

    def __iadd__(self, other: list[InlineKeyboardButton]):
        self.buttons += other
        return self
