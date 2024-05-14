class Cursor:
    def __init__(self, end: int, start=1):
        self.start = start
        self.end = end

        self.now = 1

    def __str__(self):
        return f'Страница {self.now}/{self.end}'

    def __iadd__(self, n):
        self.now = (self.now + n) % self.end
        if self.now == 0:
            self.now = self.end
        return self

    def __isub__(self, n):
        self.now = (self.now - n) % self.end
        if self.now == 0:
            self.now = self.end
        return self
