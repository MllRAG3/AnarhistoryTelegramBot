import MODULES.domain.ads_executors.util as util

try:
    import ujson as json
except ImportError:
    import json

from telebot.types import Message
from typing import Callable


class ToJson:
    def __init__(self):
        """
        Аттрибуты:

        TYPES (dict[[str, Callable]]):
          Словарь с методом преобразования под каждый тип сообщения
        jresults (tuple[str, str]):
          Результаты преобразования
        is_called (bool):
          Был ли вызван объект класса (True если да)
        """
        self.TYPES: dict[str, Callable] = {
            'text': self.text_to_dict,
            'animation': self.animation_to_dict,
            'audio': self.audio_to_dict,
            'document': self.document_to_dict,
            'photo': self.photo_to_dict,
            'video': self.video_to_dict,
        }
        self.jresults: tuple[str, str] = ('null', 'null')
        self.is_called: bool = False

    @staticmethod
    def animation_to_dict(message: Message) -> tuple[dict, dict | None]:
        """
        :param message: Информация о сообщении для преобразования
        :return: Словарь со всеми важными данными для отправки анимации
        """
        data = {
            'animation': message.animation.file_id,
            'caption': message.caption
        }

        return data, util.extract_buttons(message)

    @staticmethod
    def photo_to_dict(message: Message) -> tuple[dict, dict | None]:
        """
        :param message: Информация о сообщении для преобразования
        :return: Словарь со всеми важными данными для отправки фото
        """
        data = {
            'photo': message.photo[0].file_id,
            'caption': message.caption,
        }

        return data, util.extract_buttons(message)

    @staticmethod
    def video_to_dict(message: Message) -> tuple[dict, dict | None]:
        """
        :param message: Информация о сообщении для преобразования
        :return: Словарь со всеми важными данными для отправки видео
        """
        data = {
            'video': message.video.file_id,
            'caption': message.caption,
        }

        return data, util.extract_buttons(message)

    @staticmethod
    def text_to_dict(message: Message) -> tuple[dict, dict | None]:
        """
        :param message: Информация о сообщении для преобразования
        :return: Словарь со всеми важными данными для отправки текста
        """
        data = {
            'text': message.text,
        }

        return data, util.extract_buttons(message)

    @staticmethod
    def document_to_dict(message: Message) -> tuple[dict, dict | None]:
        """
        :param message: Информация о сообщении для преобразования
        :return: Словарь со всеми важными данными для отправки документа
        """
        data = {
            'document': message.document.file_id,
            'caption': message.caption,
        }

        return data, util.extract_buttons(message)

    @staticmethod
    def audio_to_dict(message: Message) -> tuple[dict, dict | None]:
        """
        :param message: Информация о сообщении для преобразования
        :return: Словарь со всеми важными данными для отправки документа
        """
        data = {
            'audio': message.audio.file_id,
            'caption': message.caption,
        }

        return data, util.extract_buttons(message)

    def __call__(self, message: Message) -> None:
        """
        :param message: Информация о сообщении для преобразования
        присваивает аттрибуту self.jresults результат преобразований
        :return:
        """
        try:
            to_send, buttons = self.TYPES[message.content_type](message)
        except (TypeError, KeyError):
            raise Exception(f'Данный тип сообщения не поддерживается! ({message.content_type})')
        self.jresults = json.dumps(to_send, ensure_ascii=False), json.dumps(buttons, ensure_ascii=False)
        self.is_called = True

    def __str__(self) -> str:
        """
        :return: Текст для сообщения с результатом
        """
        if not self.is_called:
            raise NotImplementedError('Перед преобразованием в строку необходимо вызвать объект класса!')

        return '<b>text:</b>\n<code>{}</code>\n\n<b>buttons:</b>\n<code>{}</code>'.format(*self.jresults)
