import MODULES.database.models.content as cntt
from MODULES.types.page import Page

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class PageLoader:
    def __init__(
            self,
            content_id: int,
            back_button: bool = False,
            main_button: bool = False,
            help_button: bool = False
    ):
        self.navigation = []
        self.load_navigation(back_button, main_button, help_button)

        self.content: cntt.Samples | None = None
        self.buttons = None
        self.load_data(content_id)

        self.markup = self.compile_buttons(InlineKeyboardMarkup())

    def load_data(self, content_id) -> None:
        try:
            self.content: cntt.Samples = cntt.Samples.get_by_id(content_id)
            self.buttons: list[cntt.Buttons] = self.content.buttons
        except AttributeError:
            raise AttributeError("УКАЗАН НЕВЕРНЫЙ ИЛИ НЕСУЩЕСТВУЮЩИЙ content_id!")

    def load_navigation(self, back_button: bool, main_button: bool, help_button: bool) -> None:
        if back_button:
            self.navigation.append(InlineKeyboardButton('<-НАЗАД-<<', callback_data='back'))
        if main_button:
            self.navigation.append(InlineKeyboardButton('ГЛАВНАЯ', callback_data='main'))
        if help_button:
            self.navigation.append(InlineKeyboardButton('ПОМОЩЬ', callback_data='help'))

    def compile_buttons(self, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
        for i in range(1, self.content.rows+1):
            row = map(lambda x: InlineKeyboardButton(x.text, callback_data=x.call_data), filter(lambda b: b.row == i, self.buttons))
            markup.row(*row)
        return markup

    def __iadd__(self, row: list[InlineKeyboardButton]):
        self.markup.row(*row)
        return self

    def __call__(self, *format_pars) -> Page:
        return Page(
            text=self.content.text.format(*format_pars),
            markup=self.markup.row(*self.navigation),
            send_format={'parse_mode': 'HTML'}
        )
