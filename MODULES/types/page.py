from typing import Any
from telebot.types import InlineKeyboardMarkup


class Page:
    def __init__(self, type, data, markup, **add):
        """
        :param text: Текст сообщения
        :param markup: Кнопки под сообщением
        """
        self.type: str = type
        self.data_json: str = data
        self.markup: InlineKeyboardMarkup = markup
        self.add: dict[str | Any] = add

    def __lshift__(self, other: dict):
        """
        Обновляет параметры отправки сообщения
        :param other: Новый словарь с параметрами отправки
        :return:
        """
        self.add = other
        return self

    @property
    def to_dict(self):
        """
        :return: Словарь для подстановки в метод TeleBot.send_message(...)
        """
        return {
            'type': self.type,
            'kwargs_json': self.data_json,
            'markup': self.markup,
            **self.add
        }
