class GraphLoader:
    def __init__(self, all_v, length=32, width=2, start=1):
        self.length = length
        self.width = width
        self.all = all_v if all_v != 0 else 1
        self.now = start

    def __iadd__(self, add):
        self.now += add
        return self

    def __call__(self):
        line = ['-'] * (self.length - 2)
        already = int(round((self.length - 2) * (self.now / self.all), 0))
        line[:already + 1] = '#' * already
        line = ['|' + ''.join(line) + '|' + f' {round((self.now / self.all) * 100, 3)}%'] * self.width

        return '\n'.join(line)
