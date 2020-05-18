from quote import Quote

class Character:
    def __init__(self, name, image, quotes, views=0):
        self._name = name           # str
        self._image = image         # str
        self._quotes = quotes       # [Quote]
        self._views = views         # int

    # name
    def get_name(self):
        return self._name

    # image
    def get_image(self):
        return self._image

    # quote
    def get_quotes(self):
        return self._quotes

    def set_quotes(self, quote):
        self._quotes.append(quote)

    # view
    def get_views(self):
        return self._views
