class Graph:
    """
    Класс для построения линейной полоски загрузки
    """
    def __init__(self, maxx, length=32, width=2):
        """
        :param maxx: Потолок загрузки (например, 100, тогда при текущем значении 100 будет 100%)
        :param length: Длина загрузочного бара в символах
        :param width: Ширина загрузочного бара в строчках (вертикально)
        """
        self.width = width
        self.length = length
        self.all = maxx
        self.now = 1

    def __iadd__(self, n):
        """
        Увеличивает текущее значение на добавляемое число
        :param n:
        :return:
        """
        self.now += n
        return self

    def __str__(self):
        """
        :return: Сгенерированный загрузочный бар с текущим значением
        """
        rep = ['-']*(self.length - 8)
        alr = int(round((self.length - 8) * (self.now / self.all)))
        rep[:alr] = ['#']*alr
        percent = round((self.now / self.all) * 100, 2)
        return '\n'.join(['|' + ''.join(rep) + f'| {str(percent).ljust(4, "0")}%'] * self.width)
