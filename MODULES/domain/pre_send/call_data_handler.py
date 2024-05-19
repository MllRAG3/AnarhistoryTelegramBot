from telebot.types import CallbackQuery


class Call:
    """
    Обработчик запросов telebot.types.CallbackQuery
    """
    def __call__(self, call: CallbackQuery, obj=None):
        """
        Ищет метод в классе obj (если != None) с названием, переданным первым словом в call;
        Вызывает его с аргументами (все остальные слова в call);
        Разделитель между словами: " "
        :param call: Объект класса telebot.types.CallbackQuery, запрос от пользователя
        :param obj: Объект любого класса в котором будет осуществляться поиск и последующий вызов метода
        :return:
        """
        name, *args = call.data.split()
        call = getattr(obj if obj else self, name, self.default_call)

        call(*args)

    @staticmethod
    def default_call(*args, **kwargs):
        pass
