class Quote:
    def __init__(self, quote, tags, views=0, likes=0):
        self._quote = quote                 # string
        self._tags = tags                    # [tags]
        self._views = views                 # int
        self._likes = likes                 # int

    # quote
    def get_quote(self):
        return self._quote

    # character
    def get_tags(self):
        return self._tags

    # view
    def get_views(self):
        return self._views

    # like
    def get_likes(self):
        return self._likes
