class Page:
    def __init__(self, text, markup, send_format: dict | None = None):
        self.text = text.replace("$NEXT", "\n")
        self.send_format = send_format
        self.markup = markup

    def __lshift__(self, other: dict | None):
        self.send_format = other
        return self

    @property
    def to_dict(self):
        return {'text': self.text, 'reply_markup': self.markup, **self.send_format}
