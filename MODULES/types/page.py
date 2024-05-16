class Page:
    def __init__(self, text, markup, send_format: dict | None = None):
        self.text = text
        self.send_format = {} if send_format is None else send_format
        self.markup = markup

    def __lshift__(self, other: dict):
        self.send_format = other
        return self

    @property
    def to_dict(self):
        return {'text': self.text, 'reply_markup': self.markup, **self.send_format}
