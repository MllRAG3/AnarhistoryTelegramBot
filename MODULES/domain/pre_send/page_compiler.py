import json

from MODULES.database.models.content import Samples
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
        self.markup: InlineKeyboardMarkup = InlineKeyboardMarkup.de_json(self.message.markup_json if self.message.markup_json != '{}' else None)

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
        a = json.loads(self.message.message_json)
        try:
            a['text'] = a['text'].format(*format_pars)
        except KeyError:
            a['caption'] = a['caption'].format(*format_pars)
        return Page(
            type=self.message.type,
            data=json.dumps(a, ensure_ascii=False),
            markup=self.markup
        )
