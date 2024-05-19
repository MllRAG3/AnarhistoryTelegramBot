class Page:
    def __init__(self, text, markup, send_format: dict | None = None):
        """
        :param text: Текст сообщения
        :param markup: Кнопки под сообщением
        :param send_format: Параметры отправки сообщения (все кроме аргументов text и reply_markup)
        """
        self.text = text
        self.send_format = {} if send_format is None else send_format
        self.markup = markup

    def __lshift__(self, other: dict):
        """
        Обновляет параметры отправки сообщения
        :param other: Новый словарь с параметрами отправки
        :return:
        """
        self.send_format = other
        return self

    @property
    def to_dict(self):
        """
        :return: Словарь для подстановки в метод TeleBot.send_message(...)
        """
        return {'text': self.text, 'reply_markup': self.markup, **self.send_format}
