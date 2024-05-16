class Graph:
    def __init__(self, maxx, length=16, width=2):
        self.width = width
        self.length = length
        self.all = maxx
        self.now = 1

    def __iadd__(self, n):
        self.now += n
        return self

    def __str__(self):
        rep = ['-']*(self.length - 2)
        alr = int(round((self.length - 2) * (self.now / self.all)))
        rep[:alr] = ['#']*alr
        percent = round((self.now / self.all) * 100, 2)
        return '\n'.join(['|' + ''.join(rep) + f'| {str(percent).ljust(4, "0")}%'] * self.width)
