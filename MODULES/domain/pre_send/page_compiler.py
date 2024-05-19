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
        self.content: Samples | None = None
        self.buttons = None
        self.load_data(content_id)

        self.markup = self.compile_buttons(InlineKeyboardMarkup())

    def load_data(self, content_id) -> None:
        """
        Загружает данные из бд (О сообщении и кнопках под ним)

        Присваивает аттрибутам:

        self.content:
          Запись из таблицы Samples с переданным ID
        self.buttons:
          Записи из таблицы Buttons, относящиеся к выбранному шаблону сообщения
        :raise: AttributeError в случае, если указан неверный content_id
        :param content_id: ID записи в таблице Samples, передается при инициализации
        :return:
        """
        try:
            self.content: Samples = Samples.get_by_id(content_id)
            self.buttons: list[Buttons] = self.content.buttons
        except AttributeError:
            raise AttributeError("УКАЗАН НЕВЕРНЫЙ ИЛИ НЕСУЩЕСТВУЮЩИЙ content_id!")

    def compile_buttons(self, markup: InlineKeyboardMarkup) -> InlineKeyboardMarkup:
        """
        Преобразовывает все записи из таблицы Buttons (атрибут slef.buttons)
        :param markup: Объект класса telebot.types.InlineKeyboardMarkup - в него будут записаны все кнопки
        :return:
        """
        for i in range(1, self.content.rows+1):
            row = map(lambda x: InlineKeyboardButton(x.text, callback_data=x.call_data), filter(lambda b: b.row == i, self.buttons))
            markup.row(*row)
        return markup

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
        self.navigation = [InlineKeyboardButton('ГЛАВНАЯ', callback_data='main')] if self.content.main_button else []
        return Page(
            text=self.content.text.format(*format_pars),
            markup=self.markup.row(*self.navigation)
        )
