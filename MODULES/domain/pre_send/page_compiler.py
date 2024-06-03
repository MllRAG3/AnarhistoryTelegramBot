from MODULES.database.models.content import Samples, Buttons
from MODULES.types.page import Page

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class PageLoader:
    """
    Класс для генерации страниц со значениями из бд
    """
    def __init__(self, content_id: int):
        """
        :param content_id: ID записи в таблице Samples
        """
        self.message: Samples = Samples.get_by_id(content_id)
        self.markup: InlineKeyboardMarkup = InlineKeyboardMarkup.de_json(self.message.markup_json)

    def __iadd__(self, row: list[InlineKeyboardButton]):
        """
        Добавляет ряд кнопок к сообщению
        :param row: Список с кнопками
        :return: Объект класса
        """
        self.markup.row(*row)
        return self

    def __call__(self, *format_pars) -> Page:
        """
        Собирает сообщение; возвращает объект типа Page
        :param format_pars: Параметры форматирования текст сообщения
        :return:
        """
        return Page(
            data=self.message.message_json.format(*format_pars),
            markup=self.markup
        )
