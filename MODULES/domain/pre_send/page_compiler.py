from MODULES.database.models.content import Samples, Buttons
from MODULES.types.page import Page

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class PageLoader:
    def __init__(
            self,
            content_id: int
    ):
        self.content: Samples | None = None
        self.buttons = None
        self.load_data(content_id)

        self.markup = self.compile_buttons(InlineKeyboardMarkup())

    def load_data(self, content_id) -> None:
        try:
            self.content: Samples = Samples.get_by_id(content_id)
            self.buttons: list[Buttons] = self.content.buttons
        except AttributeError:
            raise AttributeError("УКАЗАН НЕВЕРНЫЙ ИЛИ НЕСУЩЕСТВУЮЩИЙ content_id!")

    def compile_buttons(self, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
        for i in range(1, self.content.rows+1):
            row = map(lambda x: InlineKeyboardButton(x.text, callback_data=x.call_data), filter(lambda b: b.row == i, self.buttons))
            markup.row(*row)
        return markup

    def __iadd__(self, row: list[InlineKeyboardButton]):
        self.markup.row(*row)
        return self

    def __call__(self, *format_pars) -> Page:
        self.navigation = [InlineKeyboardButton('ГЛАВНАЯ', callback_data='main')] if self.content.main_button else []
        return Page(
            text=self.content.text.format(*format_pars),
            markup=self.markup.row(*self.navigation)
        )
